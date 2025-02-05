import matplotlib.pyplot as plt
import numpy as np


def nd_histogram(time_series, bins=10):
    """
    Return an n-dimensional histogram over a time series.
    """
    return np.histogramdd(time_series, bins=bins)[0]


def hist_entropy(hist):
    """
    Return the information entropy of a histogram.
    """
    hist = hist / np.sum(hist)
    hist = hist[hist > 0]
    entropy = -1 * np.sum(hist * np.log2(hist))
    return entropy


def redundancy_series_for_embedding(time_series, embedding_dim, max_lag=50, bins=10):
    """
    Return the redundancies of a scalar time series over a range of lag values 
    for a given embedding dimension.
    """
    redundancies = []
    for lag in range(1, max_lag + 1):
        length = len(time_series) - lag * (embedding_dim - 1)
        lagged_series = [time_series[i : i+length] for i in 
                         range(0, lag * embedding_dim, lag)]
        embedded_series = np.vstack(lagged_series).T

        entropies = (hist_entropy(nd_histogram([i], bins)) for i in lagged_series)
        joint_entropy = hist_entropy(nd_histogram(embedded_series, bins))
        redundancy = sum(entropies) - joint_entropy
        redundancies.append(redundancy)

    return redundancies


def redundancy_analysis(time_series, max_dim, max_lag=50, bins=10):
    """
    Return a matrix containing the marginal redundancies for a time series 
    across a range of time lags and embedding dimensions.

    Parameters
    ----------
    time_series : list of float or numpy.ndarray
        The scalar time series.
    max_dim : int
        The largest embedding dimension to compute.
    max_lag : int, optional
        The largest time delay to compute.
    bins : int, optional
        The number of equally-sized bins used to partition the data for 
        entropy calculations (default is 10).

    Returns
    -------
    marginal_redundancies : list of list of float
        A matrix whose rows correspond to embedding dimensions and columns 
        to time lags. The embedding dimensions range from 2 to `max_dim` 
        while the time lags range from 1 to `max_lag`.
    """
    redundancies = {1: [0] * max_lag}
    for dim in range(2, max_dim + 1):
        series = redundancy_series_for_embedding(time_series, dim, max_lag, bins)
        redundancies[dim] = series

    # Compute marginal redundancies
    marginal_redundancies = []
    for dim in range(2, max_dim + 1):
        mr = [current - prev for current, prev in 
              zip(redundancies[dim], redundancies[dim - 1])]
        marginal_redundancies.append(mr)
    
    return marginal_redundancies


def plot_marginal_redundancies(time_series, max_dim, max_lag=50, bins=10):
    """
    Plot marginal redundancy against time lag for each embedding dimension, 
    starting from m=2 up to `max_dim`.

    Parameters
    ----------
    time_series : list of float or numpy.ndarray
        The scalar time series.
    max_dim : int
        The largest embedding dimension to plot.
    max_lag : int, optional
        The largest time delay to plot on the x-axis.
    bins : int, optional
        The number of equally-sized bins used to partition the data for 
        entropy calculations (default is 10).
    """
    marginal_redundancies = redundancy_analysis(time_series, max_dim, max_lag, bins)
    
    plt.figure(figsize=(10, 6))
    for dim, values in enumerate(marginal_redundancies, start=2):
        plt.plot(range(1, max_lag + 1), values, label=f'Embedding dimension {dim}')

    plt.title('Marginal Redundancy vs Time Lag')
    plt.xlabel('Time Lag')
    plt.ylabel('Marginal Redundancy')
    plt.legend()
    plt.grid(True)
    plt.show()