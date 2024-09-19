import json
import re

filepath = 'second_comparison.json'
filepath = 'second_comparison_with_spacy_trf.json'

with open(filepath, encoding="utf-8") as json_file:
    data = json.load(json_file)



# Regular expression to find the Named_Entities section
named_entities_pattern = re.compile(r"Named_Entities\s*=\s*\[(.*?)\]", re.DOTALL)

# Initialize counters and list for true positives with respective fields
true_positives = 0
false_positives = 0
false_negatives = 0
true_positives_list = []

# Helper function to normalize entities for comparison
def normalize_entity(entity):
    return entity.lower().replace(" ", "")

# Iterate through each item in the JSON data
for item in data:
    response = item['response']
    match = named_entities_pattern.search(response)
    
    if match:
        named_entities_str = match.group(1).replace("'", "").replace(" ", "")
        named_entities = {normalize_entity(entity) for entity in named_entities_str.split(',')} if named_entities_str else set()
    else:
        named_entities = set()

    explicit_entities = {normalize_entity(entity) for entity in item['explicit_entities']}
    
    # Calculate true positives and false negatives
    for entity in explicit_entities:
        if any(entity in named_entity for named_entity in named_entities):
            true_positives += 1
            true_positives_list.append((entity, entity))
        else:
            false_negatives += 1
    
    # Calculate false positives
    for entity in named_entities:
        if not any(entity in explicit_entity for explicit_entity in explicit_entities):
            false_positives += 1

# Calculate precision and recall
precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

# Output the results
print(f"True Positives: {true_positives}")
print(f"False Positives: {false_positives}")
print(f"False Negatives: {false_negatives}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")



