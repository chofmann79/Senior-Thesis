#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 21:35:27 2024

@author: calebhofmann
"""

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

#Before importing Excel file taken directly from Bloomberg:
    #1. Delete rows 1 and 3
    #2. Rename columns 3 and 4 to "Bid_C" and "Ask_C", respectively
    #3. Rename columns 10 and 11 to "Bid_P" and "Ask_P", respectively

# Step 1: Read Excel file 
options_data = pd.read_excel("Mar13Apr24.xlsx")

# Step 2: Calculate mid prices
options_data['Call Mid'] = (options_data['Bid_C'] + options_data['Ask_C']) / 2
options_data['Put Mid'] = (options_data['Bid_P'] + options_data['Ask_P']) / 2

# Step 3: Calculate price difference
options_data['Price Difference'] = options_data['Call Mid'] - options_data['Put Mid']

# Step 4: Divide strikes by 10000 to convert Eurex strike convention to USD/JPY value
options_data['Strike'] = options_data['Strike'] 

# Step 5: Linear regression
X = options_data['Price Difference'].values.reshape(-1, 1)
y = options_data[['Strike']].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X, y)

# Step 6: Output intercept, slope, and R^2
intercept = model.intercept_[0]
slope = model.coef_[0][0]
r_squared = r2_score(y, model.predict(X))

print("Intercept:", intercept)
print("Slope:", slope)
print("R^2:", r_squared)