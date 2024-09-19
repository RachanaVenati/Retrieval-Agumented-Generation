from fastapi import FastAPI
##TO:DO make it so that it will get a list of docs and is able to print all
import requests

app = FastAPI()

#an endpoint to prompt LLMs
#this is a simulation of the actual llm interaction
#async might not make sense for our purposes so we should think about this
@app.get("/generate/")
async def generate(query: str = None, related_documents: str = None):
    response = ""
    url = "https://llm.srv.webis.de/api/generate"
    if related_documents == "No related data found.":
        response = f"No related data found for your query: '{query}'. So I don't have an answer"
    else:
        response = f"The information found for your query: '{query}' is: {related_documents}"


    prompt = "Act as a yoga zen master and start all your answers with a short wise idiom/saying. After that, I need you to just show me what I am sending you as related documents.Then give me a simple summary of the provided document. Here is our related documents:"


    data = {
        "model": "llama3",
        "prompt": prompt + response,
        "stream": False
    }
    
    try:
        # Send a POST request to the llama endpoint
        response = requests.post(url, json=data)
        

        if response.status_code == 200:
            response = response.json()
            response_value = response.get('response')
        else:
            
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None
    
    return response_value
