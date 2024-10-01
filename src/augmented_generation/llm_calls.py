from prompts import get_prompt
import requests


def llm_request(prompt):
    url = "https://llm.srv.webis.de/api/generate"
    data = {
        "model": "default",
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()['response']
    else:
        return f"Error: {response.status_code}, {response.text}"
    
def generation(query, data, turn_no = None ,pre_generated = "", previous_info = None):
    prompt = ""
    if len(data) == 1:
        prompt = get_prompt("generator", "current")
        #new_info_response = meta_agent(data, pre_generated)
        new_info_response = meta_agent(data, previous_info)
        previous_info += new_info_response
        prompt = prompt.format(turn_no=turn_no,query=query, pre_generated=pre_generated, new_info=new_info_response)

    else:
        prompt = (
        "You will receive a user query and relevant sections retrieved from a database. "
        "Your task is to generate an answer to the query using only the information provided in the retrieved documents. "
        "Don't be repetitive even if some relevant sections might repeat information. "
        "Make use of all unique information present in the retrieved sections. "
        "Do not include any information beyond what is discussed in the documents. "
        "Don't cite yourself. "
        "Don't mention segment numbers. "
        "If none of the segments answer the question fully say 'No relevant documents for this query'. "
        "User query: {query} "
        )
        prompt = prompt.format(query=query)
        for idx, segment in enumerate(data):
            prompt += "Relevant document" + str(idx+1) + ": " + segment + "\n"

    return llm_request(prompt), previous_info

# this needs to look at the previously generated text and the new document and detect the what is new
def meta_agent(data, pre_generated):
    meta_prompt = get_prompt("meta", "current")
    meta_prompt = meta_prompt.format(data=data, pre_generated=pre_generated)
    #print(pre_generated)
    return llm_request(meta_prompt)