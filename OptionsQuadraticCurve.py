#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 22:12:34 2024

@author: calebhofmann
"""

from OptionsBlackScholes import implied_volatilities
from OptionsBlackScholes import strikes2
import numpy as np
import matplotlib.pyplot as plt

# Fit a quadratic curve (2nd degree polynomial) to the data
coefficients = np.polyfit(strikes2, implied_volatilities, 2)
a, b, c = coefficients

# Generate the parabolic line using the fitted coefficients
strike_range = np.linspace(min(strikes2), max(strikes2), 100)
fitted_volatilities = a * strike_range ** 2 + b * strike_range + c

# Plot the original data and the fitted curve
plt.scatter(strikes2, implied_volatilities, label='Implied Volatilities')
plt.plot(strike_range, fitted_volatilities, color='red', label='Fitted Curve')
plt.xlabel('Strike Prices')
plt.ylabel('Implied Volatilities')
plt.title('Quadratic Curve Fitted to Implied Volatilities')
plt.legend()
plt.show()

equation = f'Implied Volatility = {a:.10f}X^2 + {b:.10f}X + {c:.10f}'
print("Equation of the fitted quadratic curve:")
print(equation)
