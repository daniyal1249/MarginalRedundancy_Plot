import matplotlib.pyplot as plt
import numpy as np

from redundancy_analysis import plot_marginal_redundancies


def rk4(func, t0, y0, dt):
    """
    Numerical integration using 4th order Runge-Kutta.
    """
    k1 = dt * func(t0, y0)
    k2 = dt * func(t0 + dt/2, y0 + k1/2)
    k3 = dt * func(t0 + dt/2, y0 + k2/2)
    k4 = dt * func(t0 + dt, y0 + k3)
    new_state = y0 + (k1 + 2*k2 + 2*k3 + k4) / 6
    return new_state


def lorenz_time_series(length, dt, transients, noise_intensity, 
                       sigma=10, beta=8/3, rho=28):
    """
    Simulate the Lorenz system and return a time series for the x state variable.

    Parameters
    ----------
    length : int
        The length of the time series after removing transients.
    dt : int
        The step size used for numerical integration.
    transients : int
        The number of transient data to discard.
    noise_intensity : float
        The strength of the additive white gaussian noise (AWGN) added to 
        the time series, given as a standard deviation.
    sigma, beta, rho : float, optional
        The parameters of the Lorenz system. The defaults are the standard 
        values.

    Returns
    -------
    x : numpy.ndarray
        The generated time series for the Lorenz system.
    """
    def lorenz_system(t, state):
        x, y, z = state
        state_derivatives = np.array([
            sigma * (y - x), 
            x * (rho - z) - y, 
            x * y - beta * z
        ])
        return state_derivatives
    
    total_length = length + transients

    x = np.empty(total_length)
    y = np.empty(total_length)
    z = np.empty(total_length)

    # Generate time series
    state = 2 * np.random.rand(3) - 1  # Random initial conditions
    x[0], y[0], z[0] = state
    for i in range(1, total_length):
        state = rk4(lorenz_system, i*dt, state, dt)
        x[i], y[i], z[i] = state
    
    # Discard transients
    x = x[transients:]

    # Add white gaussian noise
    noise = np.random.normal(0, noise_intensity, length)
    x += noise
    return x


time_series = lorenz_time_series(
    length=1_000_000, dt=0.04, transients=20_000, noise_intensity=0
    )


if __name__ == '__main__':
    # Plot the first 2500 values of the time series
    plt.figure(figsize=(12, 6))
    plt.plot(time_series[:2500])
    plt.title('Lorenz Time Series (2500 values)')
    plt.xlabel('Time Step')
    plt.ylabel('X State Variable')
    plt.grid(True)
    plt.show()

    # Plot marginal redundancy vs time lag
    plot_marginal_redundancies(time_series, max_dim=5, max_lag=50)