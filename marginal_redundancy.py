import numpy as np
import matplotlib.pyplot as plt

def nd_histogram(time_series, bins=10):
    ''' Compute an n-dimensional histogram over time_series '''
    hist = np.histogramdd(time_series, bins=bins)[0]
    return hist

def entropy_calculation(hist):
    ''' Compute information entropy of the given histogram '''
    hist = hist / np.sum(hist)
    hist = hist[hist > 0]
    entropy = -np.sum(hist * np.log2(hist))
    return entropy

def redundancy_calculation_for_embedding(vector, embedding_dim, max_lag=50, bins=10):
    ''' Compute redundancy of the provided time series for a given embedding dimension '''
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

def mr_calculation(vector, max_dim, max_lag, bins=10):
    '''
    Compute and plot marginal redundancies against time lag for each embedding dimension, starting from m=2 and going up to max_dim
    Additionally, return a matrix with rows corresponding to embedding dimension and columns to time lag
    Parameters:
        vector ((N, 1) array) - input scalar time series
        max_dim (int) - maximum embedding dimension to be used for marginal redundancy calculations
        max_lag (int) - maximum time delay to be plotted on the x-axis
        bins (int) - number of equally-sized bins taken over the range of the data for entropy calculations; default is 10
    '''
    
    all_redundancies = {1: [0] * max_lag}  # Redundancy for embedding dimension 1 is zero
    
    for dim in range(2, max_dim + 1):
        all_redundancies[dim] = redundancy_calculation_for_embedding(vector, dim, max_lag, bins)

    # Compute marginal redundancies
    marginal_redundancies = {}
    output_matrix = []
    for dim in range(2, max_dim + 1):
        marginal_redundancies[dim] = [current - prev for current, prev in zip(all_redundancies[dim], all_redundancies[dim - 1])]
        output_matrix.append(marginal_redundancies[dim])
        
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

    return np.array(output_matrix)
