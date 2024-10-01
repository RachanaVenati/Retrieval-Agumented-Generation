import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score

# Step 1: Calculate similarity scores
def calculate_similarity(X):
    return cosine_similarity(X)

# Step 2: Define virtual object representation
def virtual_object_representation(X):
    return np.mean(X, axis=0)

def modified_virtual_object_representation(X):
    w = virtual_object_representation(X)
    w_star = np.max(X, axis=0)
    w_b = 2 * w_star * w / (w_star + w)
    return w_b

# Step 3: Apply decision rule
def decision_rule(x1, x2, x_b):
    similarity = cosine_similarity([x1], [x2])[0, 0]
    threshold = max(cosine_similarity([x1], [x_b])[0, 0], cosine_similarity([x2], [x_b])[0, 0])
    return similarity if similarity > threshold else 0

# Step 4: Estimate optimal epsilon
def estimate_optimal_epsilon(X, eps_values):
    best_score = -1
    best_eps = None
    for eps in eps_values:
        clustering = DBSCAN(eps=eps).fit(X)
        if len(set(clustering.labels_)) > 1:  # Avoid single cluster
            score = silhouette_score(X, clustering.labels_)
            if score > best_score:
                best_score = score
                best_eps = eps
    return best_eps