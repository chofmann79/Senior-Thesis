#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 22:19:33 2024

@author: calebhofmann
"""

import pandas as pd
import numpy as np
from scipy.stats import norm
from OptionsLinearReg import intercept, slope
from OptionsDataImport import cleaned_strikes, cleaned_calls, interest_rate_diff, underlying

# Load intercept and slope from previous script
S_prime = intercept
B_prime = slope * -1 

desired_strikes = [float(strike) for strike in cleaned_strikes]

# Function to calculate Black-Scholes call option price
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S_prime / (K * B_prime)) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    imputed_price = S_prime * norm.cdf(d1) - K * B_prime * norm.cdf(d2)
    return imputed_price

def implied_volatility(call_price, S, K, T, r):
    tolerance = 1e-5
    max_iterations = 100
    sigma = 0.5  # Initial guess for volatility
    for _ in range(max_iterations):
        price = black_scholes_call(S, K, T, r, sigma)
        vega = S * np.sqrt(T) * norm.pdf((np.log(S_prime / (K * B_prime)) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T)))
        diff = price - call_price
        if abs(diff) < tolerance:
            return sigma
        try:
            sigma -= diff / vega
        except ZeroDivisionError:
            return np.nan  # Return NaN if division by zero occurs
    return np.nan



#Calculate implied volatility for each strike price
time_to_expiry = 0.25
interest_rate_differential = interest_rate_diff
underlying_price = underlying


implied_volatilities = []
strikes2 = []
for c, s in zip(cleaned_calls, desired_strikes):
    call_price = c
    strike_price = s
    implied_volatility_value = implied_volatility(call_price, underlying_price, strike_price, time_to_expiry, interest_rate_differential)
    implied_volatilities.append(implied_volatility_value)
    strikes2.append(strike_price)

#Output implied volatility for each exercise price
for s2, iv in zip(strikes2, implied_volatilities):
    print(s2, iv)


