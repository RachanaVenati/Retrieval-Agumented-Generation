import requests
import json

def run_llama3_api(prompt):
    url = "https://llm.srv.webis.de/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    input_file = "/home/rag/Desktop/project-rag-ss24/src/Illumulus_RAG_Component/webis-qinc-22/output.json"  
    output_file = "/home/rag/Desktop/project-rag-ss24/src/Illumulus_RAG_Component/webis-qinc-22/comparison.json"  

    with open(input_file, 'r') as infile:
        data = json.load(infile)

    results = []



    for item in data:
        title = item.get("query")

        
        if title:

            output_format = """[
            {'-named entity-': '-IOB-tag-'},
            {'-named entity-': '-IOB-tag-'},
            ...
            ...]"""

            prompt = f"""Im going to give you a title of story, I need you to find all of the named entities in the title
            (there might be more than one) and give me a list of name entities (python list format) back.
            There should be two list. One list (Named_Entities_Tags) where each of Item of the list should be a python dictionary where the key is the named entity and the value is the IOB/BIO/IOE format tag.
            So the list should be in the following format:
            {output_format}
            And another (Named_Entities) list wich only have the named entities without their tags.
            If the named entitis are made from more than one word (For instance first name and last name of a person), they should be one item.
            DO NOT WRITE any other words except the entity or entities. ONLY give me the list. So you will say "Here is the list:" and then the Named Entitites_Tags list in the format I specified and then the Named_Entities list.
            So the response should look like this:
            Here is the lists:
            Named_Entities_Tags = {output_format}
            Named_Entitites = [{'-named entity-','-named entity-',...}]
            DO NOT SAY ANY OTHER WORDS.
            If there is no named entities in the title you will give me an empty list. So you put an empty [] as the output Here is the title: {title}"""
            
        
            result = run_llama3_api(prompt)
            if result:
                response_value = result.get('response')
                if response_value:
                    response_extra = ["Here is the list:", "here is the list:","Here is the lists:", "Here are the lists:"]
                    for extra in response_extra:
                        if extra in response_value:
                            response_value = response_value.replace(extra, "")
                    output_item = {
                        "query": title,
                        "response": response_value,
                        "explicit_entities": item.get("explicit_entities", []),
                        "implicit_entities": item.get("implicit_entities", [])
                    }
                    results.append(output_item)
    #for itm in results:
    #    itm["response"]= itm["response"].replace("\n","")
    with open(output_file, 'w') as outfile:
        json.dump(results, outfile, indent=4)

if __name__ == "__main__":
    main()

