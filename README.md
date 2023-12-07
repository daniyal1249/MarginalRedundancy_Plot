# Marginal Redundancy vs Time Lag Plot
This repository generates a plot which displays the dependency of marginal redundancy $\Delta \mathcal{R}$ on time lag  $\tau$ for a time series. Theoretically, important statistical properties of the time series (i.e. Kolmogorov-Sinai entropy and accuracy of the measurements) can be estimated through visual inspection of the plot. This algorithm incorporates adjustable parameters for the number of partitions over the data, the max time lag, and max embedding dimension.

## Terminology
### Kolmogorov-Sinai Entropy
Kolmogorov-Sinai entropy, also known as measure-theoretic entropy, metric entropy, Kolmogorov entropy, or simply KS entropy, represents the information production rate of a dynamical system. For a given bin width ε, define $H_{m}$ as the information entropy of all $m$-length sequences of consecutive measurements formed from a time series with $\tau = 1$. For a time series $X_{t}$:

$$H_{m} = H(X_{t}, X_{t+1}, ..., X_{t+(m-1)})$$

$H_{m} - H_{m-1}$ then denotes the increase in entropy as the lengths of the sequences increase from $m-1$ to $m$. Physically, it represents the average amount of information needed to predict the state of the system given knowledge of the previous $m-1$ measurements. KS entropy is defined as the limit of this value, standardized for sampling rate $T$, as $N$ approaches infinity and both ε and $T$ approach zero:

$$K \equiv \lim_{T \to 0} \lim_{ε \to 0} \lim_{N \to \infty} \cfrac{1}{T}(H_{m} - H_{m-1})$$

For noiseless signals, non-chaotic systems exhibit zero KS entropy while chaotic systems display positive values. For signals containing noise, KS entropy diverges to infinity as ε approaches zero, regardless of the amount of noise present. A sufficiently large ε is chosen for practical applications in order to minimize the effect of noise and keep the value finite.

### Marginal Redundancy
To build up to the definition of marginal redundancy, the concept of mutual information will first be defined. Mutual information quantifies the amount of information one variable, or system, gives about another. In the case of this analysis, the variables are lagged versions of the original time series with increments of $\tau = 1$. Redundancy $\mathcal{R}$ is the extension of mutual information for 3 or more variables and is given by the following formula for a time series $X_t$:

$$\mathcal{R}_ {m} = \mathcal{R}(X_{t}, X_{t+1}, ..., X_{t+(m-1)}) = \left[\sum_{i=0}^{m-1} H(X_{t+i})\right] - H(X_{t}, X_{t+1}, ..., X_{t+(m-1)})$$

Marginal redundancy $\Delta \mathcal{R}_ {m}$ is then given by $\mathcal{R}_ {m} - \mathcal{R}_ {m-1}$ and represents the increase in redundancy as number of variables, or embedding dimension, increases from $m-1$ to $m$. It is important to note that $\mathcal{R}_ {1}$ is always zero, so the marginal redundancy for $m = 2$ equals  $\mathcal{R}_ {2}$.

## Python Implementation and Usage
The code takes a one-dimensional array as an input and outputs a plot with marginal redundancy on the y-axis and time lag on the x-axis. It plots a separate curve for 
![image](https://github.com/daniyal1249/MarginalRedundancy_Plot/assets/152569016/6d9053f0-a20c-4b85-b900-9d93b88b5c7a)
