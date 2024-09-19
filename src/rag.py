import requests
import sys

#this is a class for representing the retrieval pipeline on the client side
retrieval_endpoint = 'http://141.54.159.143:8000/retrieve'
generation_endpoint = 'http://127.0.0.1:8001/generate'


def main():
    if len(sys.argv) < 2:
        print("Usage: python generation.py generate 'query'")
        return
    else:
        command = sys.argv[1]
        if (command == "generate"):
            related_documents = ""
            llm_answer = ""
            try:
                query = input("Please enter your query: ")

                retrieval_response = requests.get(retrieval_endpoint, params={"query": query})
                retrieval_response.raise_for_status()  # Raises an HTTPError for 4xx or 5xx status codes
                related_documents = retrieval_response.json()
                
                generation_response = requests.get(generation_endpoint, params={"query": query, "related_documents": related_documents})
                generation_response.raise_for_status()  # Raises an HTTPError for 4xx or 5xx status codes
                llm_answer = generation_response.json()
                print(llm_answer)
                
            except requests.RequestException as e:
                print("Error:", e)
if __name__ == "__main__":
    main()