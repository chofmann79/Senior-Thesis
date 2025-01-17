#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 19:24:44 2024

@author: calebhofmann
"""

from OptionsBlackScholes import strikes2
from OptionsBlackScholes import time_to_expiry
from OptionsBlackScholes import interest_rate_differential
from OptionsBlackScholes import underlying_price
from OptionsQuadraticCurve import coefficients
from OptionsLinearReg import intercept, slope
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from OptionsDataImport import forward_rate
import math
import statistics
from scipy.interpolate import interp1d

#Load polynomial coefficients from OptionsQuadraticCurve.py
a, b, c = coefficients

def fitted_volatilities(a, b, c, K):
    fitted_vol = (a * (K ** 2)) + (b * K) + c
    return fitted_vol

def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * np.exp(-r * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

#Interpolate strikes and differentiate as per Shimko
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

# Calculate the distance from the underlying price to the furthest strike price (for symmetry)
lower_bound = underlying_price - min(strikes2)
upper_bound = max(strikes2) - underlying_price

# Find the maximum distance to ensure centering
center = max(lower_bound, upper_bound)

# Adjust the range of strike prices symmetrically around the underlying price
strike_prices = np.linspace(underlying_price - center, underlying_price + center, 1000)

strike_price_list  = []
call_option_prices = []
for K in strike_prices:
    sigma = fitted_volatilities(a, b, c, K)
    call_price = black_scholes_call(underlying_price, K, time_to_expiry, interest_rate_differential, sigma)
    call_option_prices.append(call_price)
    strike_price_list.append(K)

delta = ((underlying_price + center) - (underlying_price - center)) / 1000  
implied_probabilities = []
for C, K in zip(call_option_prices, strike_price_list):
    g = interpolation_function(time_to_expiry, interest_rate_differential, C, delta, K)
    implied_probabilities.append(g)

#Check that the total probability is equal (or close) to one
total_prob = sum(implied_probabilities) * delta
implied_probabilities = [p / total_prob for p in implied_probabilities]

#Calculating the first moment
mean3 = []
for K, P in zip(strike_price_list, implied_probabilities):
    mean4 = K * P * delta
    mean3.append(mean4)
    
mean = sum(mean3)

plt.plot(strike_price_list, implied_probabilities)
plt.xlabel('Strike Price')
plt.ylabel('Implied Probability')
plt.title('Implied Probability Distribution')
#forward_rate2 = forward_rate  # Specify the strike price where you want to add the vertical line
#plt.axvline(x=forward_rate2, color='red', linestyle='--', label='Forward Rate')
mean2 = mean
plt.axvline(x=mean2, color='green', linestyle='--', label='Mean')
plt.legend()
plt.ylim(bottom=0)
plt.show()

print("Mean:", mean)

#Calculating the second moment
variances = []
for K, P in zip(strike_price_list, implied_probabilities):
    var = ((K - mean) ** 2) * P * delta
    variances.append(var)

variances_2 = sum(variances)
print("Variance:", variances_2)

#Calculating the third moment
skews = []
for K, P in zip(strike_price_list, implied_probabilities):
    skew = (((K - mean) ** 3) * P) * delta
    skews.append(skew)

skews_2 = sum(skews) / ((variances_2 ** (3/2)))
print("Skewness:", skews_2)


#Calculating the fourth moment
kurtoses = []
for K, P in zip(strike_price_list, implied_probabilities):
    kurtosis = (((K - mean) ** 4) * P) * delta
    kurtoses.append(kurtosis)

kurtoses_2 = sum(kurtoses) / ((variances_2 ** 2))
print("Kurtosis:", kurtoses_2)

#Output strikes and implied risk-neutral densities
print(strike_price_list)
print(implied_probabilities)

