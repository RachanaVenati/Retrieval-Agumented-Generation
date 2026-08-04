# BUW at TREC 2024: Retrieval-Augmented Generation

This repository contains the Bauhaus-Universitat Weimar system for the TREC
2024 Retrieval-Augmented Generation (RAG) track. The project covers both the
retrieval task and the retrieval-augmented generation task over the MS MARCO
Segment v2.1 collection.

The system combines sparse first-stage retrieval, vector-based reranking, and
LLM answer generation with post-processed citations. The published TREC 2024
notebook paper describes the approach as a two-stage retrieval pipeline followed
by LLaMA3-based response generation.

## Tasks Covered

- Retrieval Task: retrieve the most relevant document segments for 301 TREC RAG
  queries.
- Retrieval-Augmented Generation Task: generate grounded answers from retrieved
  segments and attach citations to the supporting evidence.

## Retrieval Pipeline

The retrieval system uses two stages to balance lexical precision and semantic
matching.

### Stage 1: Pyserini BM25

- Pyserini is used with Lucene BM25 for first-stage sparse retrieval.
- BM25 retrieves the top 100 MS MARCO Segment v2.1 segments for each query.
- This stage provides a strong lexical baseline using term-frequency and query
  relevance signals.

### Stage 2: Weaviate Vector Refinement

- The top 100 BM25 segments are indexed into Weaviate.
- Segment vectors are produced with the MiniLM-based transformer vectorizer used
  by the Weaviate `text2vec-transformers` setup.
- Weaviate refines the candidate set and returns the top 20 segments.
- The system uses HNSW-style approximate nearest-neighbor search through
  Weaviate for efficient semantic retrieval.
- Two second-stage variants were explored:
  - Hybrid search, combining vector similarity with keyword/BM25-style matching.
  - Near Text search, using semantic similarity only.

The local Weaviate configuration is in `src/docker-compose.yaml`, using the
`sentence-transformers-multi-qa-MiniLM-L6-cos-v1` transformer inference image.

## Generation Pipeline

For answer generation, the system uses LLaMA3 with prompts containing:

- the original user query;
- the top 20 retrieved segments;
- instructions to ground the answer in the retrieved context;
- constraints intended to reduce hallucinated or unsupported content.

Several prompt variants were tested. Later runs used stricter prompting that
asked the model not to introduce information beyond the provided segments and to
fall back when the retrieved evidence was insufficient.

## Citation Post-Processing

Inline citation generation by the LLM was inconsistent, so citation assignment
was handled after generation.

The citation method:

1. Splits the generated answer into lines or sentences.
2. Embeds each generated unit using the same MiniLM-style sentence embedding
   approach.
3. Compares each generated unit against the retrieved segments with cosine
   similarity.
4. Adds citations for segments whose similarity exceeds the selected threshold.

This keeps generated statements traceable to retrieved evidence and improves
citation reliability compared with relying on the LLM to produce citations
directly.

### Retrieval Runs

- `dense_on_sparse`: Pyserini BM25 top-100 retrieval followed by local Weaviate
  hybrid search. The final output uses the top 20 segments.
- `weaviate_dense_base`: Pyserini BM25 top-100 retrieval followed by Weaviate
  Near Text search on a sharded Weaviate deployment with 10 shards.

For `dense_on_sparse`, the reported evaluation on adapted 2023 judgments was:

| Metric | Value |
| --- | ---: |
| Precision | 0.752 |
| NDCG average | 0.860 |

### RAG Runs

- `buw`: LLaMA3 generation over the hybrid-search retrieval output with
  structured prompting and post-processed citations.
- `buw_5`: a modified prompt focused on clearer, more concise, less repetitive
  answers, with the same citation post-processing strategy.
- `oneshot_post_sentenced`: custom stricter prompting over the Near Text
  retrieval output, with sentence-level cosine-similarity citation assignment.

## Submission Files

The submitted run outputs are stored in the following project directories:

- Retrieval submissions:
  - `src/retrieval/submission/1/r_output_trec_rag_2024.tsv`
  - `src/retrieval/submission/2/r_output_trec_rag_2024.tsv`
- Retrieval-augmented generation submissions:
  - `src/augmented_generation/submissions/1/rag_output_trec_rag_2024.jsonl`
  - `src/augmented_generation/submissions/1/output_oneshot_alt_new.jsonl`
  - `src/augmented_generation/submissions/2/rag_output_trec_rag_2024.jsonl`
  - `src/augmented_generation/submissions/2/output_oneshot_alt_subt.jsonl`

The `.tsv` files contain retrieval run outputs, while the `.jsonl` files contain
RAG generation outputs with answers, references, and citation metadata.

## Evaluation Notes

- Official TREC 2024 qrels were not available during development.
- Evaluation used TREC 2023 qrels and queries as a proxy.
- Because those qrels are document-level, the evaluation assumes that segments
  from relevant documents are relevant.
- Retrieval quality was measured with Precision and NDCG over the top 20
  retrieved segments.
- Recall was not emphasized because the project focus was ranking quality at the top of the retrieval list.

## Repository Layout

- `src/retrieval.py` and `src/retrieval/retrieval_run.py`: retrieval service and
  retrieval run logic.
- `src/tools/pyserini_retrieval.py`: Pyserini BM25 retrieval helper.
- `src/data_ingestion_weaviate/`: notebook workflow for populating and querying
  Weaviate.
- `src/augmented_generation/`: prompting, LLM calls, clustering experiments,
  citation experiments, and generation submissions.
- `src/evaluation/`: retrieval and output evaluation utilities.
- `src/docker-compose.yaml`: local Weaviate and transformer inference services.

## Core Dependencies

The main Python dependencies are listed in `requirements.txt`. They include
FastAPI, Pyserini, Weaviate client, NumPy, pandas, scikit-learn,
sentence-transformers, matplotlib, tqdm, ijson, requests, and uvicorn.
