# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 20:20:54 2022

@author: Emilio
"""
# -- Load base packages
import pandas as pd
import numpy as np
import data as dt
import pickle

# (pending) Get the list of exchanges with the symbol

# Get public trades from the list of exchanges
exchanges = ['binance']
symbol = 'BTC/USDT'

# Fetch realtime orderbook data until timer is out (60 secs is default)
orderbooks = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                           data_type='orderbooks', file_route='files/orderbooks', stop_criteria=None,
                           elapsed_secs=600, verbose=2)

# Fetch realtime orderbook data until timer is out (60 secs is default)
publictrades = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                           data_type='publictrades', file_route='files/publictrades', stop_criteria=None,
                           elapsed_secs=600, verbose=2)

with open('orderbooks2.pkl', 'wb') as f:
    pickle.dump(orderbooks, f)

with open('publictrades2.pkl', 'wb') as f:
    pickle.dump(publictrades, f)