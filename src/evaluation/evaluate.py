import weaviate
from weaviate.classes.query import MetadataQuery
from weaviate.connect import ConnectionParams
import re
from tqdm import tqdm

def extract_high_level_id(text):
    pattern = r'_(\d+)#'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

# custom client declaration 
client = weaviate.WeaviateClient(
    connection_params= ConnectionParams.from_params(
        http_host="weaviate",
        http_port="80",
        http_secure=False,
        grpc_host="weaviate-grpc",
        grpc_port="50051",
        grpc_secure=False,
    ),
)

client.connect()

collection=client.collections.get("Segments")

qrels_file_path = 'data/qrels/qrels.dl21-doc-msmarco-v2.1.txt'
qrels_dict = {}
with open(qrels_file_path, 'r') as file:
    for line in file:
        parts = line.strip().split()
        #count it when it is relevant or not non-relevant
        if (len(parts) >= 3) & (int(parts[-1]) > 1):
            key = parts[0]
            msmarco_text = parts[2]
            if key in qrels_dict:
                qrels_dict[key].append(msmarco_text)
            else:
                qrels_dict[key] = [msmarco_text]

topics_file_path = 'data/topics/topics.dl21.txt'

topics = {}

with open(topics_file_path, 'r') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            topics[parts[0]] = parts[1]

output = {}
for e in tqdm(qrels_dict, desc="Processing queries"):
    output[e] = {}
    relevant_doc_num = len(qrels_dict[e])
    topic = topics[e]
    if relevant_doc_num < 30000:
        try:
            response = collection.query.near_text(
                query=topic,
                limit=relevant_doc_num,
                return_metadata=MetadataQuery(distance=True, certainty=True)
            )
        except Exception as ex:
            print(f"Exception occurred: {ex}. Reconnecting client and retrying.")
            client.close()
            client.connect()
            response = collection.query.near_text(
                query=topic,
                limit=relevant_doc_num,
                return_metadata=MetadataQuery(distance=True, certainty=True)
            )
        #print(len(response.objects), relevant_doc_num)
        for o in response.objects:
            response_dict = {
                'url': o.properties,
                'title': o.properties['title'],
                'headings': o.properties['headings'],
                'segment': o.properties['segment'],
                'score': o.metadata.certainty
            }
            doc_level_id = extract_high_level_id(o.properties['docid'])
            output[e][doc_level_id] = response_dict

client.close()

true_positives = 0
false_negatives = 0
false_positives = 0

print('Length of topics: ', len(qrels_dict))
# Process each query
for e in tqdm(qrels_dict, desc="Processing queries"):
    results = output[e]
    qrels_docs = qrels_dict[e]
    
    # Set of relevant documents
    relevant_docs = set(doc_id.split('_')[-1] for doc_id in qrels_docs)
    
    # Set of retrieved documents
    retrieved_docs = set(results.keys())
    
    # Calculate True Positives, False Negatives, and False Positives
    true_positives += len(relevant_docs & retrieved_docs)
    false_negatives += len(relevant_docs - retrieved_docs)
    false_positives += len(retrieved_docs - relevant_docs)

# Calculate Precision and Recall
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')