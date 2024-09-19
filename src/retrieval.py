from fastapi import FastAPI
import weaviate
from weaviate.classes.config import Property,DataType
from weaviate.classes.query import Filter



##TO:DO make it so that it will return a list of docs

app = FastAPI()


client = weaviate.Client(url="http://localhost:8080")




#an endpoint to get from the documents db
#async might not make sense for our purposes so we should think about this
@app.get("/retrieve/")
async def retrieve(query: str):
    #this is a simulation of the actual vector db searc

    class_name = "Yoga"
    response = (
    client.query
    .get(class_name, ["document"])
    .with_near_text({'concepts' : [query]})
    .do()
)
    related_chunk = response['data']['Get'][class_name][0]['document']

    return related_chunk