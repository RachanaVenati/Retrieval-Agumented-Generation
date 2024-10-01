import json
import spacy

# Load the SpaCy model
nlp = spacy.load("en_core_web_sm")

def extract_named_entities(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents]
    return entities

def main():
    input_file = "H:\Bauhaus University\Term 3\RAG\project-rag-ss24\src\Illumulus_RAG_Component\webis-qinc-22\output.json"
    #input_file = "/home/rag/Desktop/project-rag-ss24/src/Illumulus_RAG_Component/webis-qinc-22/output.json"
    output_file = "H:\Bauhaus University\Term 3\RAG\project-rag-ss24\src\Illumulus_RAG_Component\webis-qinc-22\second_comparison_with_spacy.json"
    #output_file = "/home/rag/Desktop/project-rag-ss24/src/Illumulus_RAG_Component/webis-qinc-22/second_comparison_with_spacy.json"

    with open(input_file, 'r') as infile:
        data = json.load(infile)

    results = []

    for item in data:
        title = item.get("query")
        
        if title:
            named_entities = extract_named_entities(title)
            response_value = f"Named_Entities = {named_entities}"

            output_item = {
                "query": title,
                "response": response_value,
                "explicit_entities": item.get("explicit_entities", []),
                "implicit_entities": item.get("implicit_entities", [])
            }
            results.append(output_item)

    with open(output_file, 'w') as outfile:
        json.dump(results, outfile, indent=4)

if __name__ == "__main__":
    main()
