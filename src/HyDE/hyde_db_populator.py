import os
import weaviate
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests

#define file path
filePath = "yoga.txt"

#initialize text splitter
default_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100, length_function=len)

#load and split content
content = TextLoader(filePath)
sections = content.load_and_split(text_splitter=default_text_splitter)

#initialize weaviate client
client = weaviate.Client(url="http://localhost:8080")

def hypothetical_questions_generator(chunk):
    prompt = f"I am going to give you a chunk. Generate 5 possible questions for the given chunk. The chunk is: {chunk}"
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

#define the schema for the weaviate class
class_obj = {
    "class": "Yoga18",
    "properties": [
        {
            "name": "document",
            "dataType": ["text"],
        },
        {
            "name": "hypothetical_questions",
            "dataType": ["text"]
        },
    ],
    "vectorizer": "text2vec-transformers"
}

#create the class schema and add data to weaviate
try:
    client.schema.create_class(class_obj)
    for section in sections:
        hypothetical_questions = hypothetical_questions_generator(section.page_content)
        if hypothetical_questions:
            client.data_object.create(
                class_name="Yoga18",
                data_object={
                    "document": section.page_content,
                    "hypothetical_questions": hypothetical_questions["response"]
                }
            )

except (TypeError, ValueError, requests.ConnectionError, weaviate.UnexpectedStatusCodeException, weaviate.SchemaValidationException, KeyError, weaviate.ObjectAlreadyExistsException) as e:
    print(e)
