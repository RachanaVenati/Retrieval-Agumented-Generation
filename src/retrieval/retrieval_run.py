import weaviate
from weaviate.classes.query import MetadataQuery
from weaviate.exceptions import WeaviateQueryError
from weaviate.classes.init import AdditionalConfig, Timeout
from tqdm import tqdm 
import time
import numpy as np
import numpy as np
from prompts import get_prompt



client = weaviate.connect_to_custom(
    http_host="weaviatedb.srv.webis.de",  
    http_port=80,                       
    http_secure=False,   
    grpc_host="weaviateinference.srv.webis.de",  
    grpc_port=80,                       
    grpc_secure=False,
    skip_init_checks=True,
    additional_config=AdditionalConfig(
        timeout=Timeout(init=1200, query=2400, insert=1200)  # Values in seconds
    )
)
collection=client.collections.get("Segments")

topics_file_path = '../Data/topics.rag24.test.txt'

topics = {}

with open(topics_file_path, 'r') as file:
    for line in file:
        parts = line.strip().split('\t')
        if len(parts) == 2:
            topics[parts[0]] = parts[1]

topic_keys = list(topics.keys())

count = 0
q = "Q0"
type = "weaviate_dense_base"
output_file_path = '/Users/cemerturkan/Desktop/r_output_trec_rag_2024.tsv'
with open(output_file_path, 'w') as file:
    for topic_id in tqdm(topic_keys):
            
        query = topics[topic_id]
        max_retries = 4
        retries = 0
        while retries < max_retries:
            try:
                response = collection.query.near_text(
                    query=query,
                    limit=100,
                    return_metadata=MetadataQuery(distance=True, certainty=True)
                )
                break  # Break the loop if query succeeds
            except WeaviateQueryError as e:
                print(f"Query failed: {e}, retrying...")
                retries += 1
                time.sleep(2)  # Wait for 5 seconds before retrying
        object_rank = 0
        for o in response.objects:
            docid = o.properties['docid']
            certainty = o.metadata.certainty
            output = topic_id + " " + q + " " + docid + " " + str(object_rank) + " " + str(certainty) + " " + type  + "\n"
            file.write(output)
            object_rank += 1