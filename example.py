import numpy as np
import matplotlib.pyplot as plt
import marginal_redundancy as mr

def lorenz_time_series(N, dt, transients, noise_intensity, sigma=10, beta=8/3, rho=28):
    '''
    Simulate the Lorenz system and output the time series for the x state variable
    Parameters:
        N - length of time series (after transient removal)
        dt - step size
        transients - number of transient data discarded
        noise_intensity - strength (SD) of additive white gaussian noise (AWGN), standardized for SD of the time series
        sigma, beta, rho - parameters of Lorenz system; set to standard values as default
    '''
    
    def lorenz_system(t, state):
        x, y, z = state
        state_derivatives = np.array([
            sigma * (y - x),
            x * (rho - z) - y,
            x * y - beta * z
        ])
        return state_derivatives

    def rk4(func, t0, y0, dt):
        # Numerical integration using 4th order Runge-Kutta
        k1 = dt * func(t0, y0)
        k2 = dt * func(t0 + dt/2, y0 + k1/2)
        k3 = dt * func(t0 + dt/2, y0 + k2/2)
        k4 = dt * func(t0 + dt, y0 + k3)
        new_state = y0 + (k1 + 2*k2 + 2*k3 + k4) / 6
        return new_state

    state = np.random.rand(3) * 2 - 1  # Random initial conditions
    x = np.empty(N + transients)
    y = np.empty(N + transients)
    z = np.empty(N + transients)
    x[0], y[0], z[0] = state
    
    for i in range(1, N + transients):
        state = rk4(lorenz_system, i*dt, state, dt)
        x[i], y[i], z[i] = state
    
    x_transients_removed = x[transients:]

    # White gaussian noise is added to the time series
    sd_x = np.std(x_transients_removed)
    noise = np.random.normal(0, noise_intensity * sd_x, N)
    x_transients_removed = x_transients_removed + noise

    return x_transients_removed

time_series = lorenz_time_series(N=1000000, dt=0.04, transients=20000, noise_intensity=0)

# Plot the first 2500 values of the time series
plt.figure(figsize=(12, 6))
plt.plot(time_series[:2500])
plt.xlabel('Time Steps')
plt.ylabel('X State Variable')
plt.title('Lorenz Time Series (First 2500 Values)')
plt.grid(True)
plt.show()

# Plot marginal redundancy vs time lag
mr.mr_calculation(time_series, max_dim=5, max_lag=50, bins=10)
