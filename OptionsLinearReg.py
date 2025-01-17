#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:35:27 2024

@author: calebhofmann
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from OptionsDataImport import cleaned_strikes, cleaned_calls, cleaned_puts

print(cleaned_strikes)
print(cleaned_calls)
print(cleaned_puts)

price_diff = [a - b for a, b in zip(cleaned_calls, cleaned_puts)]

price_diff = pd.DataFrame(price_diff)

strikes = pd.DataFrame(cleaned_strikes)

X = price_diff.values.reshape(-1, 1)
y = strikes.values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Step 6: Output intercept, slope, and R^2
intercept = model.intercept_[0]
slope = model.coef_[0][0]
r_squared = r2_score(y, model.predict(X))

print("Intercept:", intercept)
print("Slope:", slope)
print("R^2:", r_squared)