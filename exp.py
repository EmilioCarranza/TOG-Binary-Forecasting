# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 20:20:54 2022

@author: Emilio
"""
# test
# -- Visualization
import data as dt

# (pending) Get the list of exchanges with the symbol

# Get public trades from the list of exchanges
exchanges = ['binance']
symbol = 'BTC/USDT'

# Fetch realtime orderbook data until timer is out (60 secs is default)
orderbooks = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                           data_type='orderbooks', file_route='Files/orderbooks', stop_criteria=None,
                           elapsed_secs=60, verbose=2)

# Fetch realtime orderbook data until timer is out (60 secs is default)
publictrades = dt.async_data(symbol=symbol, exchanges=exchanges, output_format='inplace', timestamp_format='timestamp',
                             data_type='publictrades', file_route='Files/publictrades', stop_criteria=None,
                             elapsed_secs=120, verbose=2)
