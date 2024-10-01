
from pyserini.search.lucene import LuceneSearcher
import json

# Load the pre-downloaded index
index_path = '/mnt/ssd1/ssd_lucene_indexes/lucene-index.msmarco-v2-doc-segmented-full.20220808.4d6d2a'
searcher = LuceneSearcher(index_path, "msmarco-v2-doc-segmented-full")

# Load the JSON array from a file
input_file = '/home/rag/Desktop/project-rag-ss24/src/finale/test topics retreival/topics_rag24_test.json'
output_file = '/mnt/ssd1/topics_final_r_segments.json'
query_batch_size = 50  # Number of queries to process in each batch
result_batch_size = 500  # Number of results to write in each batch,


with open(input_file, 'r') as f:
    queries_dict = json.load(f)

# Function to process a batch of queries
def process_query_batch(query_batch):
    results = []
    for query_obj in query_batch:
        query = query_obj['query']
        num_hits = 1000
        hits = searcher.search(query, num_hits)

        # Collect results
        for hit in hits:
            docid = hit.docid
            score = hit.score
            raw = searcher.doc(docid).raw()
            raw_data = json.loads(raw)
            result = {
                'docid': raw_data.get('docid', ''),
                'url': raw_data.get('url', ''),
                'title': raw_data['title'],
                'headings': raw_data['headings'],
                'segment': raw_data['segment'],
            }
            results.append(result)

            # Write each result as a JSON line
            with open(output_file, 'a') as out_f:
                json.dump(result, out_f)
                out_f.write('\n')
        
# Divide the list of queries into chunks and process each chunk
for i in range(0, len(queries_dict), query_batch_size):
    query_batch = queries_dict[i:i + query_batch_size]
    process_query_batch(query_batch)
    

print("Search results written to", output_file)