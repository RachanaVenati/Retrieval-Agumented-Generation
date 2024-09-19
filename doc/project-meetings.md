# Diving Deep into Retrieval Augmented Generation (RAG)
Project Meetings

## Week 1. April 16, 2024.
- [x] Welcome.
- [x] Working at Webis.
- [x] Main Project Goals.
- [x] InfoBot Demo.

## Week 2. April 24, 2024.
lead: Cem, master: Armin.
- [x] Clone this repository on your computer using git. Put your Discord name next to your Email address on the main page and push the change.
- [x] Create an [Overleaf](https://www.overleaf.com/) project for a potential [ECIR](https://ecir2025.eu/) paper and enable link-sharing. Share the link with the group. [Link to the paper](https://www.overleaf.com/2771336927snycrccrskpy#6af3ed)
- [x] Go through the [SIGIR 2024 conference proceedings](https://dblp.org/db/conf/sigir/sigir2023.html) and find all papers dealing with RAG. Put the respective bib entries to the overleaf paper, and list all the titles in a Related Work section.
- [x] Inform yourself about the [Meta Comprehensive RAG Benchmark Challenge](https://www.aicrowd.com/challenges/meta-comprehensive-rag-benchmark-kdd-cup-2024). Be able to explain how the challenge works.
- [x] Get yourself familiar with [fast api](https://fastapi.tiangolo.com/). Design an API for (1) the RAG retrieval component and (2) the RAG generation component. Align the API with existing standards (see [OLLama](https://ollama.com/)).
- [x] Do one of the following [short courses](https://www.deeplearning.ai/short-courses/). Put your name next to the bullet point. Be able to answer questions about the course contents.
  - [x] Armin https://www.deeplearning.ai/short-courses/preprocessing-unstructured-data-for-llm-applications/
  - [ ] https://www.deeplearning.ai/short-courses/building-applications-vector-databases/
  - [x] Rachana https://www.deeplearning.ai/short-courses/large-language-models-semantic-search/
  - [x] Husain https://www.deeplearning.ai/short-courses/advanced-retrieval-for-ai/
  - [ ] https://www.deeplearning.ai/short-courses/vector-databases-embeddings-applications/
  - [x] Cem https://www.deeplearning.ai/short-courses/knowledge-graphs-rag/
  - [x] Yokesh https://www.deeplearning.ai/short-courses/langchain-chat-with-your-data/,
  - [ ] https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/
  - [ ] https://www.deeplearning.ai/short-courses/build-llm-apps-with-langchain-js/
  - [ ] https://www.deeplearning.ai/short-courses/javascript-rag-web-apps-with-llamaindex/
  - [x] Mohammad https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/

## Week 3. May 1, 2024 (public holiday).
lead: Armin, master: Cem.

- [x]	Registering in the Meta Comprehensive RAG Benchmark Challenge and get theire sample data. Check if we are able to use the data legally.
- [x]	Fast API implementation.
- [x]	Figuring out what type of DB we are going to use for our retrieval endpoint (Make a list of pros and cons)
- [ ]	Try to store the data from Meta in the DB
- [x]	Delve into the illumulus project and see how we can add a RAG component.
- [x]	RAG from scratch course

## Week 4. May 8, 2024.
lead: Armin, master: Cem.

- [x] FastAPI updates Prof. Gollub mentioned
- [x] Add weaviate querying to our retrieval endpoint
- [ ] Storing data in weaviate
- [x] Going through related papers and come up with research question

## Week 5. May 15, 2024.
lead: Mohammad, master: Rachana.

- [x] Query translation (wikification or wikify) extracting information from the query using the api or the llm.

- [x] Indexing pipeline for weaviate which takes input (Json) and index it in the DB. This includes figuring out:
    How do we do the Vectorization,
    Check weather Weaviate has a vectorization module.

- [x] Side Task: Having the generation replaced with requesting llm response and adding a Readme.md to the repo.

## Week 6. May 22, 2024.
lead: Husain, master: Mohammad.

- [x] Evaluating the result of the NER- Evaluation of llama3 entity performance.
(Dealing with multiple documents with the same named entity/title)

- [ ] Take prompts used in Illumulus and Augment Our code with the prompts.

- [x] Finishing the indexing pipeline by storing the competition dataset and benchmarking.

- [ ] Do research on retrieval augmented diffusion. (Task for everyone)

- [x] Document Everything in the repository. It is Good to have a Readme in each of the folders and keep the repository updated. (Task for everyone)

- [x] Side Task: Looking into TREC Competition. (For Everyone)

## Week 7. May 29, 2024.
lead: Yokesh, master: Husain.

- [x]  Finish the evaluation by calculating the precision and recall (The model results for webis qinc dataset and the story titles) and check for the wikipedia pages
- [x]  Augument our code with illumulus
- [x]  Connect to the webis vpn to hit the llm in the building  (Everyone)
- [x]  Put everything into the vector database and Qrels evaluation
- [ ]  Valid submission file for the first or second or both tasks
- [x]  HyDE- generate questions based on chunks, index and retrieve

## Week 8. June 5, 2024.
lead: Rachana, master: Yokesh.

- [x]  Finish the evaluation by calculations of prec, recall on the named entities of qinc dataset and illumulus story titles
- [x]  Prepare a comparison between llama and Spacy on NER
- [x]  Evaluate the result of illumulus (we can try to evaluate the entity overlap b/w generated story and the wikipedia article ) and look into entity linking. Also coming up with a criteria for evaluting the generated stories.
- [x] Try to index 100 million vectors (random) to weaviate and request time to answer (embed with ollama endpoint if not we have to go with gamma web solution)
- [x] Indexing the portion of the dataset (1 mBs)  of TREC and measure time
  •	Llama3 embedding (embedding dimensions)
  •	Current local option (embedding dimentsions)
- [x] Benchmarking with HyDE and without HyDE
  •	Compare similarity metric bw. the two options(cosine by default)
  •	LLM-as-a-judge
  •	10 query each 30 query in total human-as-a-judge

## Week 9. June 12, 2024.
  lead:Cem, master: Armin.

  - [ ] Figure out a way to solve ambiguous entities.
  - [x] Try to reduce the latency ( → compare latency of getting the whole story at once and getting each section individually)
  - [ ] Improve the prompt for using the information from wikipedia
  - [x] Add the final function to a new branch of illumulus repo
---------------------
  - [ ] Check tutorials about sentence Bert.
  - [ ] Docker program that vectorise and sends data(Docker note book container for gpu).
  - [ ] Go through papers on how to embed data for dense retrieval.
  - [ ] Use qrels for the Hyde evaluation.


## Week 10. June 19, 2024.
  lead:Armin, master: Cem.

  - [ ] Figure out a way to solve ambiguous entities.
  - [x] Improve the prompt for using the information from wikipedia
  - [x] Improve German story generation
  - [x] Figure out a way for handling multiple entities in one title
---------------------

## Week 11. June 26, 2024.
  lead:Husain, master: Mohammad.

  - [ ] Solving Ambiguous Entities:

  Check if spaCy provides solutions for solving ambiguous entities using entity categories.
  Check the frequency of ambiguous entities.
  Examine the relation of ambiguous entities with the other parts of the title.

  - [x] Preventing LLM from Deviation:

  Fix the code to prevent the large language model (LLM) from generating content that deviates from the intended story.

  - [ ] Interface for Ambiguous Entities:

  Work on the interface to handle and resolve ambiguous entities.

  - [x] Enhancing Image Generation for Illumulus: Investigate retrieval-augmented diffusion models to improve image generation.

---------------------

- [x] With ssd on, try the retrieval on pyserini.
- [x] put retrieved segments to weaviate.
- [x] set up gpu cluster for dense retrieval.
- [x] prepare output file for submission.

## Week 12. July 03, 2024.
  lead:Rachana, master: Mohammad.

  - [x] Inhancing image generation and improve the relation between the story and the picture by using other images.

      Check out the version 3 of stable defusion.
      See how the paper embedded the images.

  - [x] How do we fill the small length of the input context prompt of the defusion model in a way we capture the most information from the story and the wiki summary?

---------------------
- [ ] check evaluation using TREC evaluation library.
- [ ] Embedding files needs to be created on gpu cluster.

## Week 13. July 10, 2024.
  lead: Yokesh, master: Rachana.

- [x] Change the request process of getting images from wiki
- [x] Retrieving images:  Check out bing search and scrapping google image for picture retrival. 
- [x] Preventing LLM from Deviation: Fix the code to prevent the large language model (LLM) from generating text that deviates from the intended story.
---------------------
- [ ] Top20-100 segments and try to increase the metrics
- [ ] NDCG tool- ranking and relevance based evaluation
- [ ] Top5-for RAG and check relevance score.

## Week 14. July 17, 2024.
  lead: Cem, master: Armin.

- [x] Add the charachters to the image captions and add the summary of the story to the prompt for image generation
- [ ] Fix the timeout situation 
- [x] Make it stable 
- [ ] Preventing LLM from deviation: Fix the code to prevent the large language model (LLM) from generating text that deviates from the intended story
- [ ] Implement the pixel api
---------------------
- [ ] be done with the weaviate db population.
- [ ] run the evaluation code with the full dataset.
- [ ] create a rag prototype for trec.
- [ ] use relevance scores and check the evaluation metrics.

## Week 15. July 24, 2024.
No Meeting

## Week 16. July 31, 2024.
- [ ] Look for academic accesses of image search engines
- [ ] Check out available image databases with context online
- [ ] Create our own image database using Wikipedia images
---------------------
- [ ] Evaluate on all evaluation sets (dl21, dl22, dl23, dev, dev2, raggy, researchy)
- [ ] Experiment with reranking
