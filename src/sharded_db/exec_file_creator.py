import os
import re
import tarfile
import time
import json

def extract_batch(file_name):
    # Define the regex pattern to match the number before '.pt'
    pattern = r'_(\d+)\.pt'
    # Search for the pattern in the file name
    match = re.search(pattern, file_name)
    if match:
        # Return the matched number
        return int(match.group(1))
    else:
        # Return None or handle the case where no match is found
        return None

def extract_number(file_name):
    # Define the regex pattern to match the number before '.json'
    pattern = r'_(\d+)\.json'
    # Search for the pattern in the file name
    match = re.search(pattern, file_name)
    if match:
        # Return the matched number
        return "_" + match.group(1) + "_"
    else:
        # Return None or handle the case where no match is found
        return None

def find_files_with_number(embeddings_path, number):
    files = {}
    for root, dirs, filenames in os.walk(embeddings_path):
        for filename in filenames:
            if number in filename:
                batch_num = extract_batch(filename)
                files[batch_num] = os.path.join(root, filename)
    return files

tar_file_path = "/data/ceph/storage/data-tmp/current/kavo1286/rag/msmarco_v2.1_doc_segmented.tar"
embeddings_path = "/data/ceph/storage/data-tmp/current/kavo1286/rag/embeddings/"
exec_files = {}

# Open the tar file
with tarfile.open(tar_file_path, 'r') as tar:
    start_time = time.time()
    # Iterate through the members of the tar file
    for member in tar.getmembers():
        matching_files = {}
        number = extract_number(member.name)
        if number:
            matching_files = find_files_with_number(embeddings_path, number)
        exec_files[member.name] = matching_files
    elapsed_time = time.time() - start_time
    print(elapsed_time)

# Remove the first key-value pair
if exec_files:
    first_key = next(iter(exec_files))
    exec_files.pop(first_key)

# Export the exec_files dictionary as a JSON object
with open('exec_files.json', 'w') as json_file:
    json.dump(exec_files, json_file)