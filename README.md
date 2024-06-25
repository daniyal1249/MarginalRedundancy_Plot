# Marginal Redundancy vs Time Lag Plot
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This repository generates a plot which displays the dependency of marginal redundancy $\Delta \mathcal{R}$ on time lag  $\tau$ for a time series. Theoretically, important statistical properties of the time series (i.e. Kolmogorov-Sinai entropy and accuracy of the measurements) can be estimated through visual inspection of the plot. This algorithm incorporates adjustable parameters for the number of partitions over the data, the max time lag, and max embedding dimension.

## Terminology

### Marginal Redundancy
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;To begin, it is crucial to understand the concept of redundancy for a collection of time series. Redundancy $\mathcal{R}$ is the extension of mutual information for 3 or more random variables. It quantifies the amount of information that is shared among the variables. In the case of this analysis, the variables are the time series $X_t$ and its lagged counterparts with time increments of $\tau$ ($X_{t+\tau}, X_{t+2\tau}, ...$). Redundancy is defined as the following, where $H(X)$ is the Shannon entropy of time series $X$ with partitions $x_1, x_2,..., x_n$:

$$\mathcal{R}_ {m}(\tau) = \mathcal{R}(X_{t}, X_{t+\tau}, ..., X_{t+(m-1)\tau}) = \left[\sum_{i=0}^{m-1} H(X_{t+i\tau})\right] - H(X_{t}, X_{t+\tau}, ..., X_{t+(m-1)\tau}),$$

$$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Marginal redundancy $\Delta \mathcal{R}_ {m}$ is then given by $\mathcal{R}_ {m} - \mathcal{R}_ {m-1}$ and represents the increase in redundancy as number of variables, or embedding dimension, increases from $m-1$ to $m$. It is important to note that $\mathcal{R}_ {1}$ is zero, so the marginal redundancy at $m = 2$ equals  $\mathcal{R}_ {2}$.

### Kolmogorov-Sinai Entropy
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Kolmogorov-Sinai entropy, also known as measure-theoretic entropy, metric entropy, Kolmogorov entropy, or simply KS entropy, represents the information production rate of a dynamical system. For a given bin width ε, define $H_{m}$ as the information entropy of all $m$-length sequences of consecutive measurements formed from a time series. For a time series $X_{t}$:

$$H_{m} = H(X_{t}, X_{t+1}, ..., X_{t+(m-1)})$$

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; $H_{m} - H_{m-1}$ then denotes the increase in entropy as the lengths of the sequences increase from $m-1$ to $m$. Physically, it represents the average amount of information needed to predict the state of the system given knowledge of the previous $m-1$ measurements. KS entropy is defined as the limit of this value, standardized for step size $\Delta t$, as embedding dimension $m$ approaches infinity and both ε and $\Delta t$ approach zero:

$$K := \lim_{\Delta t \to 0} \lim_{ε \to 0} \lim_{m \to \infty} \cfrac{1}{\Delta t}(H_{m} - H_{m-1})$$

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the absence of noise, non-chaotic systems exhibit zero KS entropy while chaotic systems generate positive values. For signals containing noise, KS entropy diverges to infinity as ε approaches zero, regardless of the amount of noise present. In practical applications, a sufficiently large ε is chosen in order to minimize the effect of noise and keep the value finite.

## Python Script Overview
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The python function 'marginal_redundancies_calculation' takes in a time series array with the specified parameters (max_dim, max_lag, bins) and outputs a plot with marginal redundancy on the y-axis and time lag on the x-axis. It plots a separate curve for each embedding dimension starting from $m=2$ up to 'max_dim' over the time lags $\tau=1$ to 'max_lag'. 

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;An example is shown below for the Lorenz system using 1,000,000 data points. The parameters and time series generation function are included in example.py. The computation time is approximately 30 seconds on an Intel® Core™ i7-1255U at base clock speed.

![image](https://github.com/daniyal1249/MarginalRedundancy_Plot/assets/152569016/6d9053f0-a20c-4b85-b900-9d93b88b5c7a)

## Plot Inspection
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In the marginal redundancy plot, the curves should converge to a straight line relation for sufficiently large embedding dimension:

$$\Delta \mathcal{R}_ {m}(\tau) = c - K\tau$$

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The negative of the slope of this asymptote line is the KS entropy of the system. 

## Installation & Packages

- **Installation:** Download marginal_redundancy.py in your project directory and import the file as a Python module using import marginal_redundancy.

- **Required Packages:** numpy, matplotlib


## References

[1]  A. M. Fraser, “Using Mutual Information to Estimate Metric Entropy,” Springer series in synergetics, pp. 82–91, Jan. 1986, doi: https://doi.org/10.1007/978-3-642-71001-8_11.

[2]  A. M. Fraser, “Information and entropy in strange attractors,” IEEE Transactions on Information Theory, vol. 35, no. 2, pp. 245–262, Mar. 1989, doi: https://doi.org/10.1109/18.32121.

[3]  M. Palus, "Kolmogorov Entropy From Time Series Using Information-Theoretic Functionals," Neural Network World, vol. 7, 1997.

[4]  Y. Sinai, “Kolmogorov-Sinai entropy,” Scholarpedia, vol. 4, no. 3, p. 2034, 2009, doi: https://doi.org/10.4249/scholarpedia.2034.

[5]  G. P. Williams, “Chaos Theory Tamed,” CRC Press eBooks, Sep. 1997, doi: https://doi.org/10.1201/9781482295412.

