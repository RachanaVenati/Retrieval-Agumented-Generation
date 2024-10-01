import weaviate
import os
import torch
from weaviate.classes.config import Configure, Property, DataType
from weaviate.connect import ConnectionParams
from weaviate.classes.query import MetadataQuery
from tqdm import tqdm
import tarfile
import time
import gzip
import json

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

print("The connection is live: ", client.is_live())

client.collections.create(
    "Segments",
    vectorizer_config= Configure.Vectorizer.text2vec_transformers(),
)
collection=client.collections.get("Segments")

tar_file_path = "/data/ceph/storage/data-tmp/current/kavo1286/rag/msmarco_v2.1_doc_segmented.tar"
embeddings_path = "/data/ceph/storage/data-tmp/current/kavo1286/rag/embeddings/"
exec_files = {}
# This file manages the mapping of the embeddings to the raw data
with open("exec_files.json", 'r') as json_file:
    exec_files = json.load(json_file)

error_messages = []
failed_docids = []
processed = []

with tarfile.open(tar_file_path, 'r') as tar:
        start_time = time.time()
        for raw_file in list(exec_files.keys()):
                embedding_batch_index = 0
                processed.append(raw_file)
                extracted_file = tar.extractfile(raw_file)
                # This sorts the batch numbers mapped to the raw data so that line 
                # by line processing is possible
                reading_order = sorted(list(exec_files[raw_file].keys()), key=int)
                batch_num = reading_order[embedding_batch_index]
                print("Processing " + raw_file + "...")
                aggregation = collection.aggregate.over_all(total_count = True)
                print("Processed files are: ", processed)
                print("# of Items inside the db: ", aggregation.total_count)
                data_path = exec_files[raw_file][batch_num]
                data = torch.load(data_path, map_location=torch.device('cpu'))
                with gzip.open(extracted_file, 'rt', encoding='utf-8') as gz:
                        with collection.batch.dynamic() as batch:
                                for counter, line in tqdm(enumerate(gz), total=int(reading_order[-1])):
                                        # Allow for skipping to the next batch of embeddings
                                        if (counter >= int(batch_num)) & (embedding_batch_index <len(reading_order)-1):
                                                embedding_batch_index += 1
                                                batch_num = reading_order[embedding_batch_index]
                                                print(batch_num)
                                                data_path = exec_files[raw_file][batch_num]
                                                data = torch.load(data_path, map_location=torch.device('cpu'))
                                        line_json = json.loads(line)
                                        docid = line_json['docid']
                                        try:
                                                batch.add_object(properties ={
                                                                        'docid': docid,
                                                                        'url': line_json['url'],
                                                                        'title' :  line_json['title'],
                                                                        'headings' : line_json['headings'],
                                                                        'segment' : line_json['segment'],
                                                                        'start_char' : line_json['start_char'],
                                                                        'end_char' : line_json['end_char'],
                                                                },
                                                                vector = data[docid],
                                                        )
                                        except Exception as e:
                                                # Append the docid and the error message to the respective lists
                                                failed_docids.append(docid)
                                                error_messages.append(str(e))
                aggregation = collection.aggregate.over_all(total_count = True)
                print(aggregation.total_count)

print(error_messages)
elapsed_time = time.time() - start_time
print("elapsed time: ", elapsed_time)

print(collection.shards())

response = collection.query.near_text(
    query="what is a shark?",
    limit=2,
    return_metadata=MetadataQuery(distance=True, certainty=True)
)

for o in response.objects:
    print(o.properties)
    print(o.metadata.certainty)
    print(o.metadata.distance)
client.close()