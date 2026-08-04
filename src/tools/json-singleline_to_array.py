#convert single line json to json array
import json

input_file_path = '/mnt/ssd1/pyserini_r_final_segments/topics_final_r_segments_unique.json'
output_file_path = '/mnt/ssd1/pyserini_r_final_segments/topics_final_r_segments_unique_array.json'

with open(output_file_path, 'w', encoding='utf-8') as outfile:
    outfile.write('[\n')
    
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        first_line = True
        for line in infile:
            try:
                json_obj = json.loads(line.strip())
                if not first_line:
                    outfile.write(',\n') 
                else:
                    first_line = False
                json.dump(json_obj, outfile, indent=4)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line}\n{e}")
    
    outfile.write('\n]')
