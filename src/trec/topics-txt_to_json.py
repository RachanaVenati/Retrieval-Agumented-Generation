import json
#converts .txt to .json 
input_file_path = '/home/rag/Desktop/project-rag-ss24/src/finale/test topics retreival/topics_rag24_test.txt'
output_file_path = '/home/rag/Desktop/project-rag-ss24/src/finale/test topics retreival/topics_rag24_test.json'

data_list = []

with open(input_file_path, 'r', encoding='utf-8') as file:
    for line in file: 
        id_str, query = line.split('\t', 1)
        data_dict = {
            'id': id_str,
            'query': query.strip()
        }
        data_list.append(data_dict)

with open(output_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, indent=4)

print(f"Data has been successfully written to {output_file_path}")