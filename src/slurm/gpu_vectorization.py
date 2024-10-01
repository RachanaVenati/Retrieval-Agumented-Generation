import tarfile
import gzip
import ujson as json
import torch
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import tqdm
import cProfile
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Check if a GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load the model
model = SentenceTransformer('sentence-transformers/multi-qa-MiniLM-L6-cos-v1')

model = model.to(device)


if device == "cuda":
    model.half()


# Function to get embeddings for a batch of texts
def get_embeddings_batch(texts):
    with torch.no_grad():
        batch_embeddings = model.encode(texts, convert_to_tensor=True)
    
    return batch_embeddings



# Function to process a batch of JSON lines
def process_json_lines_batch(json_lines):
    docids = [json.loads(line)['docid'] for line in json_lines]
    texts = [json.loads(line)['segment'] for line in json_lines]
    embeddings = get_embeddings_batch(texts)
    return {docids[i]: embeddings[i] for i in range(len(docids))}
    
def batch_chef(gz):
    batch = []
    for line in gz:
        batch.append(line.strip())
    return batch



batch_size = 2048
record_limit = 100352
embedding_dict = {}
tar_file_path = 'msmarco_v2.1_doc_segmented.tar'


# Open the tar file
with tarfile.open(tar_file_path, 'r') as tar:
    start_time = time.time()
    # Iterate through the members of the tar file
    for member in tar.getmembers():
        if member.name.endswith('.json.gz') :
            extracted_file = tar.extractfile(member)
            if extracted_file is not None:
                # Open the .json.gz file using gzip
                with gzip.open(extracted_file, 'rt', encoding='utf-8') as gz:
                    batch = []
                    count = 0
                    for line in gz:   
                        #executor = ThreadPoolExecutor(max_workers = 32)
                        batch.append(line.strip())
                        if len(batch) == batch_size:
                            embedding_dict.update(process_json_lines_batch(batch))
                            batch = []
                            count += batch_size
                            if (count >= record_limit) & ((count % record_limit) == 0):
                                #save pickle file for  record_limit times segment
                                file_name = member.name.split('/')[1].split('.json')[0]
                                file_name += "_" + str(count) + ".pt"
                                torch.save(embedding_dict, "embeddings/" + file_name)
                                
                                embedding_dict = {}

                                elapsed_time = time.time() - start_time
                                print(f"Processed {count} lines in {elapsed_time} seconds.")
                                #gatekeeper
                                #if count > record_limit:
                                    #break
                    # Process any remaining lines in the final batch
                    if batch:
                        embedding_dict.update(process_json_lines_batch(batch))
                        
                        file_name = member.name.split('/')[1].split('.json')[0]
                        file_name += "_" + str(count) + ".pt"
                        torch.save(embedding_dict, "embeddings/" + file_name)
                        
                        embedding_dict = {}
                        count += len(batch)
                        print(f"Processed {count} lines in total in the file. {member.name.split('/')[1].split('.json')[0]}")
            