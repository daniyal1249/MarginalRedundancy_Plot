# Marginal Redundancy vs Time Lag Plot

This repository generates a plot which displays the dependency of marginal 
redundancy $\Delta \mathcal{R}$ on time lag $\tau$ for a time series. 
Theoretically, important statistical properties of the time series 
(i.e. Kolmogorov-Sinai entropy and accuracy of the measurements) can be 
estimated through visual inspection of the plot. This algorithm incorporates 
adjustable parameters for the number of bins over the data, the max time lag, 
and max embedding dimension.

## Terminology

### Shannon Entropy

Let $X_t$ be a vector time series. Assume a partition $\xi$ of the state space 
of $X_t$ into bins $\\{x_1, x_2, ..., x_n\\}$, where each $x_i$ represents a 
specific range of values $X_t$ can take. The Shannon entropy of $X_t$ over 
partition $\xi$ is given by:

$$
H(X_t) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)
$$

where $P(x_i)$ is the probability of the time series values falling into the 
bin $x_i$.

### Redundancy and Marginal Redundancy

Consider a scalar time series $X_t$. Let $(X_{t}, X_{t+\tau}, ..., X_{t+(m-1)\tau})$ 
be the time delay embedding of $X_t$ in an $m$-dimensional state space with 
time lag $\tau$. The redundancy $\mathcal{R}$, also known as total correlation, 
of this vectorized time series with respect to a partition $\xi$ is given by:

$$
\mathcal{R}_ {m}(\tau) = \mathcal{R}(X_{t}, X_{t+\tau}, ..., X_{t+(m-1)\tau}) = 
\left[\sum_{i=0}^{m-1} H(X_{t+i\tau})\right] - H(X_{t}, X_{t+\tau}, ..., 
X_{t+(m-1)\tau})
$$

Like mutual information, this quantity represents the average amount of 
information that is shared, or redundant, among the time series of interest. 
Marginal redundancy $\Delta \mathcal{R}_ {m}$ is then defined as 
$\mathcal{R}_ {m} - \mathcal{R}_ {m-1}$ and denotes the increase in redundancy 
as the embedding dimension increases from $m-1$ to $m$. It is important to note 
that $\mathcal{R}_ {1} = 0$, so the marginal redundancy at $m = 2$ equals 
$\mathcal{R}_ {2}$.

### Kolmogorov-Sinai Entropy

Kolmogorov-Sinai entropy, also known as measure-theoretic entropy, metric 
entropy, Kolmogorov entropy, or simply KS entropy, represents the information 
production rate of a dynamical system. For a given partition, define $H_{m}$ 
as the Shannon entropy of all $m$-length sequences of consecutive measurements 
formed from a time series. For a time series $X_{t}$:

$$
H_{m} = H(X_{t}, X_{t+1}, ..., X_{t+(m-1)})
$$

$H_{m} - H_{m-1}$ then denotes the increase in entropy as the lengths of the 
sequences increase from $m-1$ to $m$. Physically, it represents the average 
amount of information needed to predict the state of the system given knowledge 
of the previous $m-1$ measurements. KS entropy is defined as the limit of this 
value, standardized for step size $\Delta t$, as the embedding dimension $m$ 
approaches infinity and both the bin width $\epsilon$ and $\Delta t$ approach 
zero:

$$
K := \lim_{\Delta t \to 0} \lim_{\epsilon \to 0} \lim_{m \to \infty} 
\cfrac{1}{\Delta t}(H_{m} - H_{m-1})
$$

In the absence of noise, non-chaotic systems exhibit zero KS entropy while 
chaotic systems display positive values. For signals containing any amount of 
noise, KS entropy diverges to infinity as $\epsilon$ approaches zero. In 
practical applications, a sufficiently large $\epsilon$ is chosen in order to 
minimize the effect of noise and prevent the value from diverging.

## Python Script Overview

The python function `plot_marginal_redundancies` takes in a scalar time series 
array with the specified parameters (`max_dim`, `max_lag`, `bins`) and outputs 
a plot with time lag on the x-axis and marginal redundancy on the y-axis. It 
plots a separate curve for each embedding dimension starting from $m=2$ up to 
`max_dim` over the time lags $\tau=1$ to `max_lag`. 

An example is shown below for the Lorenz system using 1,000,000 data points. 
The parameters and time series generation function are included in 
`example.py`. The computation time is approximately 30 seconds on an Intel® 
Core™ i7-1255U at base clock speed.

![Image](Example/lorenz_mr_plot.png)

## Plot Inspection

In the marginal redundancy plot, the curves should converge to a straight line 
relation for sufficiently large embedding dimension:

$$
\Delta \mathcal{R}_ {m}(\tau) = c - K\tau
$$

The negative of the slope of this asymptote line approximates the KS entropy 
of the system. 

## Installation & Packages

- **Installation:** Download `redundancy_analysis.py` in your project directory 
and import the file as a Python module using `import redundancy_analysis`.

- **Required Packages:** `numpy`, `matplotlib`

## References

[1]  A. M. Fraser, “Using Mutual Information to Estimate Metric Entropy,” 
Springer series in synergetics, pp. 82–91, Jan. 1986, 
doi: https://doi.org/10.1007/978-3-642-71001-8_11.

[2]  A. M. Fraser, “Information and entropy in strange attractors,” IEEE 
Transactions on Information Theory, vol. 35, no. 2, pp. 245–262, Mar. 1989, 
doi: https://doi.org/10.1109/18.32121.

[3]  M. Palus, "Kolmogorov Entropy From Time Series Using Information-Theoretic 
Functionals," Neural Network World, vol. 7, 1997.

[4]  Y. Sinai, “Kolmogorov-Sinai entropy,” Scholarpedia, vol. 4, no. 3, 
p. 2034, 2009, doi: https://doi.org/10.4249/scholarpedia.2034.

[5]  G. P. Williams, “Chaos Theory Tamed,” CRC Press eBooks, Sep. 1997, 
doi: https://doi.org/10.1201/9781482295412.
