from weaviate.classes.config import Configure, Property, DataType

# Create a collection and define properties
# Note that you can use `client.collections.create_from_dict()` to create a collection from a JSON object
client.collections.create(
    "Article",
    properties=[
        Property(name="title", data_type=DataType.TEXT),
        Property(name="body", data_type=DataType.TEXT),
    ]
)

# Specify a vectorizer for a collection.
vectorizer_config=Configure.Vectorizer.text2vec_openai()


# Create an object
Article = client.collections.get("Article")

uuid = Article.data.insert({
    "question": "Whats is the name of this vector DB?",
    # "answer": "Weaviate",  # properties can be omitted
    "newProperty": 123,  # will be automatically added as a number property
})

print(uuid)  # the return value is the object's UUID


data_rows = [
    {"title": f"Object {i+1}"} for i in range(5)
]




# Basic batch import
collection = client.collections.get("YourCollection")

with collection.batch.dynamic() as batch:
    for data_row in data_rows:
        batch.add_object(
            properties=data_row,
        )