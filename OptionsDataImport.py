#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 14:54:53 2024

@author: calebhofmann
"""

import pandas as pd
from datetime import datetime, timedelta
import math

#Set the date from which you would like to pull options data.
date = datetime(2022, 12, 20)

#Set the expiry of the options for which you would like data.
expiry_date = date + timedelta(days=90)

#Pull other relevant data 
bsd = pd.read_excel("BlackScholes Data.xlsx")
bsd.set_index(bsd.columns[0], inplace=True)
bsd.index = pd.to_datetime(bsd.index)
interest_rate_diff = bsd.loc[date, "Interest Rate Differential"]
underlying = 10000 / bsd.loc[date, "USDJPY"]
forward_rate = bsd.loc[date, "Forward Rate"]

#Selects the correct month's excel file
if expiry_date.month == 1:
    file = "JADF.xlsx"
elif expiry_date.month == 2:
    file = "JADG.xlsx"
elif expiry_date.month == 3:
    file = "JADH.xlsx"
elif expiry_date.month == 4:
    file = "JADJ.xlsx"
elif expiry_date.month == 5:
    file = "JADK.xlsx"
elif expiry_date.month == 6:
    file = "JADM.xlsx"
elif expiry_date.month == 7:
    file = "JADN.xlsx"
elif expiry_date.month == 8:
    file = "JADQ.xlsx"
elif expiry_date.month == 9:
    file = "JADU.xlsx"
elif expiry_date.month == 10:
    file = "JADV.xlsx"
elif expiry_date.month == 11:
    file = "JADX.xlsx"
elif expiry_date.month == 12:
    file = "JADZ.xlsx"

#Selects the correct year tab within the chosen excel file
if expiry_date.year == 2017:
    sheet_name = file.replace(".xlsx", "") + "7"
elif expiry_date.year == 2018:
    sheet_name = file.replace(".xlsx", "") + "8"
elif expiry_date.year == 2019:
    sheet_name = file.replace(".xlsx", "") + "9"
elif expiry_date.year == 2020:
    sheet_name = file.replace(".xlsx", "") + "0"
elif expiry_date.year == 2021:
    sheet_name = file.replace(".xlsx", "") + "1"
elif expiry_date.year == 2022:
    sheet_name = file.replace(".xlsx", "") + "2"
elif expiry_date.year == 2023:
    sheet_name = file.replace(".xlsx", "") + "3"
elif expiry_date.year == 2024:
    sheet_name = file.replace(".xlsx", "") + "4"


target_date = date 
df = pd.read_excel(file, sheet_name=sheet_name)

# Filter the row where the date matches
row = df[df['Dates'] == target_date]

strike_to_call = {}
strike_to_put = {}

for column in df.columns:
    parts = column.split()  # Split the column name into parts
    if 'Curncy' in column:
      strike_price = parts[1]  # The price is the second part of the column name
      if 'C' == parts[0][-1]:  # Call option
          strike_to_call[strike_price] = float(row[column])
      elif 'P' == parts[0][-1]:  # Put option
          strike_to_put[strike_price] = float(row[column])

# Initialize lists to store the data
strike_prices = []
call_prices = []
put_prices = []

for strike in strike_to_call.keys():
  # Ensure the strike price exists in both dictionaries
  if strike in strike_to_put:
      strike_prices.append(strike)                 # Append the strike price
      call_prices.append(strike_to_call[strike]) # Append the corresponding call price
      put_prices.append(strike_to_put[strike])   # Append the corresponding put price


    
def clean_lists(strike_prices, call_prices, put_prices):
    # Create new lists by filtering out 'nan' values in calls or puts
    new_strikes = []
    new_calls = []
    new_puts = []
    
    for strike, call, put in zip(strike_prices, call_prices, put_prices):
        # Check if the call or put is 'nan' using math.isnan for floats
        if not (math.isnan(call) or math.isnan(put)):
            new_strikes.append(strike)
            new_calls.append(call)
            new_puts.append(put)

    return new_strikes, new_calls, new_puts

cleaned_strikes, cleaned_calls, cleaned_puts = clean_lists(strike_prices, call_prices, put_prices)




