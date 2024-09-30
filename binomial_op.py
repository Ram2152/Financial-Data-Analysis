import numpy as np

def binomial_option_price(S, K, T, r, sigma, N, option_type='call', american=False):
    """
    Binomial Option Pricing Model for European/American Call and Put Options.
    
    Parameters:
    S: Initial stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free interest rate
    sigma: Volatility (standard deviation of stock returns)
    N: Number of time steps
    option_type: 'call' for Call option, 'put' for Put option
    american: Boolean. True for American option, False for European option.
    
    Returns:
    option_price: Price of the option
    """
    dt = T / N  # Time step size
    u = np.exp(sigma * np.sqrt(dt))  # Up movement factor
    d = 1 / u  # Down movement factor
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability
    
    # Initialize asset prices at maturity
    asset_prices = np.zeros(N + 1)
    for i in range(N + 1):
        asset_prices[i] = S * (u ** i) * (d ** (N - i))
    
    # Initialize option values at maturity
    option_values = np.zeros(N + 1)
    if option_type == 'call':
        option_values = np.maximum(0, asset_prices - K)  # Call option payoff
    elif option_type == 'put':
        option_values = np.maximum(0, K - asset_prices)  # Put option payoff
    
    # Backward induction to calculate option price
    for j in range(N - 1, -1, -1):
        for i in range(j + 1):
            option_values[i] = np.exp(-r * dt) * (p * option_values[i + 1] + (1 - p) * option_values[i])
            if american:  # If it's an American option, check for early exercise
                if option_type == 'call':
                    option_values[i] = np.maximum(option_values[i], asset_prices[i] - K)
                elif option_type == 'put':
                    option_values[i] = np.maximum(option_values[i], K - asset_prices[i])
    
    return option_values[0]

# Example usage:
S = 100  # Initial stock price
K = 105  # Strike price
T = 1  # Time to maturity (1 year)
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility (20%)
N = 100  # Number of time steps

# Price of a European Call option
european_call_price = binomial_option_price(S, K, T, r, sigma, N, option_type='call', american=False)
print(f"European Call Option Price: {european_call_price:.2f}")

# Price of an American Put option
american_put_price = binomial_option_price(S, K, T, r, sigma, N, option_type='put', american=True)
print(f"American Put Option Price: {american_put_price:.2f}")
