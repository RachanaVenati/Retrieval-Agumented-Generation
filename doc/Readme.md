# Diving Deep into Retrieval Augmented Generation (RAG)
Documentation.

![Advanced RAG piepline](https://cdn.hashnode.com/res/hashnode/image/upload/v1713375387925/9246942a-79e4-4d94-b032-a85f10480a99.png "Advanced RAG piepline")
[image source](https://www.freecodecamp.org/news/mastering-rag-from-scratch/)

## Overviews
- [Retrieval-Augmented Generation for AI-Generated Content: A Survey](https://arxiv.org/abs/2402.19473v1)
- [ACL 2023 Tutorial: Retrieval-based Language Models and Applications](https://acl2023-retrieval-lm.github.io/)
- [RAG courses on deeplearning.ai](https://www.deeplearning.ai/short-courses/)
- [RAG course on AI Makerspace](https://www.youtube.com/playlist?list=PLrSHiQgy4VjGQohoAmgX9VFH52psNOu71)

## RAG Frameworks
- LlamaIndex
- LangChain/Graph
- [Verba](https://github.com/weaviate/Verba)
- [Prompt Flow](https://github.com/microsoft/promptflow)

## The retrieval component
- Processing different kinds of documents.
  - [Short Course](https://learn.deeplearning.ai/courses/preprocessing-unstructured-data-for-llm-applications)
  - [Unstructured PDF Text Extraction](https://medium.com/@khadijamahanga/unstructured-pdf-text-extraction-3a20db14791e)
  - [Unstructured | The Unstructured Data ETL for Your LLM](https://unstructured.io/)
  - [LlamaIndex Pdf Extractor](https://www.llamaindex.ai/blog/mastering-pdfs-extracting-sections-headings-paragraphs-and-tables-with-cutting-edge-parser-faea18870125)
- Sparse vs. dense retrieval.
- turning the user request into a search query.

## The generation component
- prompt engineering.
- how to incorporate the search results into the prompt.
- how to enable quoting from the retrieved documents.

## The agent component
 - [Agentic Design Patterns](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance/?utm_campaign=The%20Batch&utm_source=hs_email&utm_medium=email&_hsenc=p2ANqtz-8Kh954rkXmE4vgpKvro3Klpjhn7IuT-Y_eXIYtgVIq9PTzwa5zFWX7FZZqv1tuDEEsTDuY)

## The evaluation component
- [Ragas](https://docs.ragas.io/en/latest/concepts/metrics/index.html)
- [Webinar - Fix Hallucinations in RAG Systems with Pinecone and Galileo](https://www.rungalileo.io/blog/fix-hallucinations-in-rag-systems-with-pinecone-and-galileo)

## API Dev
- The aim of this API is to replicate the capabilities of [ollama](https://github.com/ollama/ollama)
- Endpoints for retrieval of documents and generation of LLM response are gonna be hosted on different systems so they are in separate FastAPI apps/scripts.
- rag.py is the "main" script that coordinates the logic of communicating with the endpoints.
- The below guides are reproduceable definitely for macos or linux but terminal/command line commands might need some tweaking for windows
- The generation endpoint sends a request to "https://llm.srv.webis.de/api/generate" which has a local instance of LLaMa3 70b 
- The retrieval endpoint retrieves from the docker container of a weaviate vector db that contains chunks of the sample document about yoga. (refer to https://github.com/selva86/datasets/blob/master/yoga_raw.txt for the sample data)

- To set up a virtual environment and install dependencies of the project:
  1. cd /path/to/project
  2. set up a virtual environment with the name venv with python version == Python 3.11.6
  3. pip install -r requirements.txt

- To test the current state of the API:
  1. First run our containers on the docker-desktop app(to overcome the docker-desktop bug----> systemctl --user force-reload docker-desktop)
  2. go to our project directory(Desktop/project-rag-ss24) and then activate the venv with source venv/bin/activate 
  3. navigate to src
  4. run "uvicorn retrieval:app --reload --port 8000" on one terminal
  5. run "uvicorn generation:app --reload --port 8001" on another terminal
  6. There is one functionality built in as of now.
    - run "python rag.py generate <query>" where queries will return a chunk from the sample document "yoga.txt" which will be sent to the generation endpoint which will then return the answer from the llm.

