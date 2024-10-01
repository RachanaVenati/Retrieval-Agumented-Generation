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
    output_file = "/home/rag/Desktop/project-rag-ss24/src/Illumulus_RAG_Component/webis-qinc-22/second_comparison.json"  

    with open(input_file, 'r') as infile:
        data = json.load(infile)

    results = []



    for item in data:
        title = item.get("query")

        
        if title:

            # output_format = """[
            # {'-named entity-': '-IOB-tag-'},
            # {'-named entity-': '-IOB-tag-'},
            # ...
            # ...]"""

            prompt = f"""Im going to give you a title of story, I need you to find all of the named entities in the title (there might be more than one) and give me a list of name entities (python list format) back. First, here are some definitions of named entities:
            On the level of entity extraction, Named Entities (NE) were defined as proper names and quantities of interest. Person, organization, and location names were marked as well as dates, times, percentages, and monetary amounts[CHI 98].
            The Named Entity task consists of three subtasks (entity names, temporal expressions, number expressions). The expressions to be annotated are unique identifiers of entities (organization, persons, locations), times (dates, times), and quantities (monetary values, percentages) [CHI 97].
            Named entities are phrases that contain the names of persons, organizations and locations [TJO 03].
            While no standard definition exists, NE may be said to constitute a particular type of lexical unit referring to a real-world entity in certain specific domains, notably the human, social, political, economic and geographic domains, and which have a name (typically a proper noun or an acronym) [MEU 04].
            Named entities traditionally include three broad classes: names, quantities, and dates and durations. We will consider named entities in the context of information retrieval (entities, relationships) where they are used to constitute a knowledge base [ROS 11].
            PAY Attention to these definitions. If a words is not an entity based on these definitions it should not be listed in the Named_Entity list.
            
            So your answer should be one list. (Named_Entities) list which only have the named entities that you find in the title.
            DO NOT WRITE any other words except the entity or entities. ONLY give me the list. So you will say "Here is the list:" and then the and then the Named_Entities list.
            So the response should look like this:
            Here is the lists:
            Named_Entitites = [{'-named entity-','-named entity-',...}]
            DO NOT SAY ANY OTHER WORDS.
            If there is no named entities in the title you will give me an empty list. So you put an empty [] as the output.
            Here is the title: {title}"""
            
        
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

