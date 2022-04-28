
#packages
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pickle
from scipy.stats import kurtosis
import matplotlib.pyplot as plt
from matplotlib import pyplot
import ccxt

# import orderbooks and publictrades with pickle.
orderbooks_file = open('orderbooks2.pkl', 'rb')
orderbooks = pickle.load(orderbooks_file)
print(orderbooks)
orderbooks_file.close()

publictrades_file = open('publictrades2.pkl', 'rb')
publictrades = pickle.load(publictrades_file)
print(publictrades)
publictrades_file.close()

# Basic data check
publictrades['binance'].keys()
orderbooks['binance'].keys()
orderbooks_list = list(orderbooks['binance'])[0]
type(list(orderbooks['binance'])[0])

