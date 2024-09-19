import requests
import wikipediaapi
import json

def request_llama3(prompt):
    url = "https://llm.srv.webis.de/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        # Send a POST request to the API endpoint
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


    entity_list = []
    filepath = 'illumulus_story_titles.json'
    wiki_wiki = wikipediaapi.Wikipedia('RagProj', 'en')
    with open(filepath, encoding="utf-8") as json_file:
        data = json.load(json_file)
    for key in data:

        title = data[key]
        prompt = f"Im going to give you a title of story, I need you to find one named entity in the title and only give me that names entity back (if the entity is two or more words give all of them). Do not write any other words except the entity. If there is no named entities in the title just . Some titles are in german. When you encounter this, translate the title to english, and give me the entity.  Here is the title: {title}"

        result = request_llama3(prompt)
        response_value = result.get('response')
        entity_list.append(response_value)

    json.dumps({'extracted_entities': entity_list})
    with open('story_titles_entities.json', 'w') as f:
        json.dump(data, f)


    output_format = """[
    {'-named entity-': '-IOB-tag-'},
    {'-named entity-': '-IOB-tag-'},
    ...
    ...]"""
    title = input("Enter the title for your story: ")
    prompt = f"""Im going to give you a title of story, I need you to find all of the named entities in the title
    (there might be more than one) and only give me a list of name entities (python list format) back.
    Each of Item of the list should be a python dictionary where the key is the named entity and the value is the IOB/BIO/IOE format tag.
    So the list should be in the following format:
    {output_format}
    If the named entitis are made from more than one word (For instance first name and last name of a person), they should be one item.
    DO NOT WRITE any other words except the entity or entities. I repeat, ONLY give me the list.
    If there is no named entities in the title you will give me an empty list. Here is the title: {title}"""
    

    result = request_llama3(prompt)
    response_value = result.get('response')
    print(response_value)
    #wiki_wiki = wikipediaapi.Wikipedia('RagProj', 'en')
    #page_py = wiki_wiki.page(response_value)
    #print("Page title: " , page_py.title)
    #print("Page summary: " , page_py.summary)

if __name__ == "__main__":
    main()

