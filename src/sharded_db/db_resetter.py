import json
import weaviate
from weaviate.connect import ConnectionParams

client = weaviate.WeaviateClient(
    connection_params= ConnectionParams.from_params(
        http_host="weaviate",
        http_port="80",
        http_secure=False,
        grpc_host="weaviate-grpc",
        grpc_port="50051",
        grpc_secure=False,
    ),
)

client.connect()

collection=client.collections.get("Segments")
aggregation = collection.aggregate.over_all(total_count=True)
print(aggregation.total_count)

with open("exec_files.json", 'r') as json_file:
    exec_files = json.load(json_file)

client.collections.delete("Segments")
client.close()