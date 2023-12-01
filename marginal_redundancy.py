import numpy as np
import matplotlib.pyplot as plt

def nd_histogram(time_series, bins=10):
    # Computes an n-dimensional histogram over time_series
    hist = np.histogramdd(time_series, bins=bins)[0]
    return hist

def entropy_calculation(hist):
    # Computes information entropy of the given histogram
    hist = hist / np.sum(hist)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))
    return entropy

def redundancy_calculation_for_embedding(vector, embedding_dim, max_lag=50, bins=10):
    # Computes redundancy of the provided time series for a given embedding dimension
    redundancies = []
    for lag in range(1, max_lag + 1):
        max_length = len(vector) - lag * (embedding_dim - 1)
        datasets = [vector[i:i + max_length] for i in range(0, lag * embedding_dim, lag)]
        datasets_transposed = np.vstack(datasets).T

        # Compute entropies
        entropies = sum(entropy_calculation(nd_histogram([d], bins)) for d in datasets)
        joint_entropy = entropy_calculation(nd_histogram(datasets_transposed, bins))
        
        redundancy = entropies - joint_entropy
        redundancies.append(redundancy)
    
    return redundancies

def marginal_redundancies_calculation(vector, max_dim=5, max_lag=50, bins=10):
    # Computes and plots marginal redundancies against time lag for embedding dimensions up to max_dim
    all_redundancies = {1: [0] * max_lag}  # Redundancy for embedding dimension 1 is zero
    
    for dim in range(2, max_dim + 1):
        all_redundancies[dim] = redundancy_calculation_for_embedding(vector, dim, max_lag, bins)

    # Computes marginal redundancies
    marginal_redundancies = {}
    for dim in range(2, max_dim + 1):
        marginal_redundancies[dim] = [current - prev for current, prev in zip(all_redundancies[dim], all_redundancies[dim - 1])]
    
    # Plot
    plt.figure(figsize=(10, 6))
    for dim, values in marginal_redundancies.items():
        plt.plot(range(1, max_lag + 1), values, label=f"Embedding Dimension {dim}")

    plt.xlabel('Time Lag')
    plt.ylabel('Marginal Redundancy')
    plt.title('Marginal Redundancy vs Time Lag')
    plt.legend()
    plt.grid(True)
    plt.show()

# Compute and plot marginal redundancies
# Replace time_series with your time series data
marginal_redundancies_calculation(time_series, max_dim=5, max_lag=50, bins=10)