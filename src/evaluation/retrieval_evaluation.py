import pandas as pd
import numpy as np

# Load the TSV files into DataFrames
qrel_file = 'qrels_rag24_raggy-dev.tsv'  # Replace with your qrel file path
output_file = 'output_results_top5.tsv'  # Replace with your output file path

qrel_df = pd.read_csv(qrel_file, sep='\t', header=None, names=['query_num', 'doc_id', 'relevance'])
output_df = pd.read_csv(output_file, sep='\t', header=None, names=['query_num', 'doc_id'])

# Initialize dictionaries to store the metrics
precision_scores = {}
recall_scores = {}
f1_scores = {}
ndcg_scores = {}

# Get the unique queries
queries = qrel_df['query_num'].unique()

# Function to calculate DCG
def dcg(relevance_scores):
    return np.sum(relevance_scores / np.log2(np.arange(2, len(relevance_scores) + 2)))

# Function to calculate NDCG
def ndcg(relevance_scores):
    ideal_dcg = dcg(sorted(relevance_scores, reverse=True))
    if ideal_dcg == 0:
        return 0.0
    return dcg(relevance_scores) / ideal_dcg

# Calculate metrics for each query
for query in queries:
    # Relevant documents for the query with their relevance scores
    relevant_docs = qrel_df[qrel_df['query_num'] == query][['doc_id', 'relevance']].set_index('doc_id')['relevance'].to_dict()
    
    # Retrieved documents for the query
    retrieved_docs = output_df[output_df['query_num'] == query]['doc_id']
    
    # True Positives (TP): Relevant documents that were retrieved
    tp = len(set(relevant_docs.keys()) & set(retrieved_docs))
    # False Positives (FP): Non-relevant documents that were retrieved
    fp = len(set(retrieved_docs) - set(relevant_docs.keys()))
    # False Negatives (FN): Relevant documents that were not retrieved
    fn = len(set(relevant_docs.keys()) - set(retrieved_docs))
    
    # Precision: TP / (TP + FP)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    # Recall: TP / (TP + FN)
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    # F1 Score: 2 * (Precision * Recall) / (Precision + Recall)
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Relevance scores for the retrieved documents in the order they were retrieved
    relevance_scores = [relevant_docs.get(doc_id, 0) for doc_id in retrieved_docs]
    # Calculate NDCG
    ndcg_score = ndcg(relevance_scores)
    
    # Store the metrics
    precision_scores[query] = precision
    recall_scores[query] = recall
    f1_scores[query] = f1
    ndcg_scores[query] = ndcg_score

# Convert the metrics dictionaries to DataFrames for better readability
metrics_df = pd.DataFrame({
    'Query': precision_scores.keys(),
    'Precision': precision_scores.values(),
    'Recall': recall_scores.values(),
    'F1 Score': f1_scores.values(),
    'NDCG': ndcg_scores.values()
})

# Display the metrics for each query
print(metrics_df)

# Optionally, save the metrics to a TSV file
metrics_df.to_csv('evaluation_metrics_top5_NDCG.tsv', sep='\t', index=False)