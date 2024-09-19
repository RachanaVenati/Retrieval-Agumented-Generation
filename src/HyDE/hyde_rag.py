import weaviate
import requests

#connect to the weaviate instance
client = weaviate.Client("http://localhost:8080")

#prompt user for input
user_query = input("Please enter your story title: ")

#query weaviate for the relevant document
response = (
    client.query
    .get("Yoga18", ["document"])
    .with_near_text({"concepts": [user_query]})
    .with_limit(3)
    .do()
)

#extract information from the response
information = response["data"]["Get"]["Yoga18"][0].get("document")
print("Retrieved information:", information)

#define the function to generate a summary
def generate_summary(user_query, information):
    prompt = f"I am going to give you a topic and information related to that topic. Write a summary about the topic from the information given. Here is the topic: {user_query} and its relevant information: {information}"
    url = "https://llm.srv.webis.de/api/generate"
    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    try:
        #send a POST request to the API endpoint
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

#generate the summary
summary_response = generate_summary(user_query, information)
if summary_response:
    print("Generated summary:", summary_response.get("response"))
