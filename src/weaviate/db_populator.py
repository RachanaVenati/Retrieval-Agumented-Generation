import os
import weaviate
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
import time

filePath = "yoga.txt" 
default_text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=100,length_function=len)
content = TextLoader(filePath)
sections = content.load_and_split(text_splitter=default_text_splitter)
client = weaviate.Client(url="http://localhost:8080")
class_obj = {
    "class" : "Yoga",
    "properties": [
        {
            "name": "document",
            "dataType": ["text"],
        },
    ],
    "vectorizer": "text2vec-transformers" 
}
try:
    start_time = time.time()
    client.schema.create_class(class_obj)
    for section in sections:
        client.data_object.create(
            class_name="Yoga",
            data_object={
                "document" : section.page_content
            }
        )
    print("--- %s seconds ---" % (time.time() - start_time))
except (TypeError,ValueError,requests.ConnectionError,weaviate.UnexpectedStatusCodeException,weaviate.SchemaValidationException,KeyError,weaviate.ObjectAlreadyExistsException) as e:
    print(e)