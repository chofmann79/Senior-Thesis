#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 13:20:04 2024

@author: calebhofmann
"""

from OptionsBlackScholes import strikes
from OptionsBlackScholes import time_to_expiry
from OptionsBlackScholes import interest_rate_differential
from OptionsBlackScholes import underlying_price
from OptionsQuadraticCurve import coefficients
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


a, b, c = coefficients

def fitted_volatilities(a, b, c, K):
    fitted_vol = (a * (K ** 2)) + (b * K) + c
    return fitted_vol

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * np.exp(-r * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def interpolation_function(T, r, C, delta, K):
    K_plus = K + delta
    K_minus = K - delta
    
    C1_vol = fitted_volatilities(a, b, c, K_plus)
    C3_vol = fitted_volatilities(a, b, c, K_minus)
    
    C1 = black_scholes_call(underlying_price, K_plus, T, r, C1_vol)
    C3 = black_scholes_call(underlying_price, K_minus, T, r, C3_vol)

    factor = np.exp(r * T)
    numerator = factor * (C1 + C3 - (2 * C))
    denominator = delta ** 2
    g = numerator / denominator
    
    return g

strike_prices = np.linspace(min(strikes), max(strikes), 1000)

strike_price_list  = []
call_option_prices = []
for K in strike_prices:
    sigma = fitted_volatilities(a, b, c, K)
    call_price = black_scholes_call(underlying_price, K, time_to_expiry, interest_rate_differential, sigma)
    call_option_prices.append(call_price)
    strike_price_list.append(K)

delta = (max(strikes) - min(strikes)) / 1000  
implied_probabilities = []
for C, K in zip(call_option_prices, strike_price_list):
    g = interpolation_function(time_to_expiry, interest_rate_differential, C, delta, K)
    implied_probabilities.append(g)
    
converted_strikes = []
for i in strike_price_list:
    new_strike = 10000 / i
    converted_strikes.append(new_strike)

plt.plot(converted_strikes, implied_probabilities)
plt.xlabel('Strike Price')
plt.ylabel('Implied Probability')
plt.title('Implied Probability Distribution')
forward_rate = 147.039  # Specify the strike price where you want to add the vertical line
plt.axvline(x=forward_rate, color='red', linestyle='--', label='Forward Rate')
plt.legend()
plt.show()

