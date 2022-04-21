# Repositorios
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import pickle
from scipy.stats import kurtosis
import matplotlib.pyplot as plt
from matplotlib import pyplot
import ccxt

# import orderbooks and publictrades with pickle.
orderbooks_file = open('orderbooks.pkl', 'rb')
orderbooks = pickle.load(orderbooks_file)
print(orderbooks)
orderbooks_file.close()

publictrades_file = open('publictrades.pkl', 'rb')
publictrades = pickle.load(publictrades_file)
print(publictrades)
publictrades_file.close()

# Check keys and see if data is ok.
publictrades['binance'].keys()
orderbooks['binance'].keys()
orderbooks_list = list(orderbooks['binance'])[0]
type(list(orderbooks['binance'])[0])

# Spread ask price - bid price
path_orderbooks = orderbooks['binance'][list(orderbooks['binance'])[2]]
spread = path_orderbooks['ask_price'][0] - path_orderbooks['bid_price'][0]
puntos_base = spread * 10000  # puntos base

# spread , mid-price (promedio entre ask y bid)
midprice = (path_orderbooks['ask_price'][0] + path_orderbooks['bid_price'][0]) * .05

# weighted midprice como midprice pero multiplicados por los volumenes
weighted_midprice = ((path_orderbooks['ask_price'][0]) * (path_orderbooks['ask_vol'][0]) + (
        (path_orderbooks['bid_price'][0]) * (path_orderbooks['bid_vol'][0]))) * .05

# volumen total bid volume y ask volume, se suman para el total
total_bid_volume = (path_orderbooks['bid_vol']).sum()
total_ask_volume = (path_orderbooks['ask_vol']).sum()
Dif_bid_ask = total_bid_volume - total_ask_volume

# Microprice vol ask / total volume precio medio ponderado por el volumen
orderbookinbalance = total_ask_volume / (total_bid_volume + total_ask_volume)
microprice = midprice * orderbookinbalance

# volume weighted average price (VWAP) cada precio se multiplica por el volumen y se divide entre el volumen total
priceask = (orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_price'])
pricebid = (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price'])
volumeask = (orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_vol'])
volumebid = (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_vol'])

vwap_bid = []
for i in range(100):
    vwap_bid1 = (pricebid[i] * volumebid[i]) / total_bid_volume
    vwap_bid.append(vwap_bid1)

vwap_ask = []
for i in range(100):
    vwap_ask1 = (priceask[i] * volumeask[i]) / total_ask_volume
    vwap_ask.append(vwap_ask1)
imb_dif = total_bid_volume - total_ask_volume
# statics , spread midprice, weighted mid price , total volume, bid volume, ask volume
# dynamics diff midprice( diferencia entre dos mid prices), midprice return valor final - valor inicial,
# sign(midprice return)
# 2nd order variance (midprice return)

# trade-flow, volume-flow

# volume per unit of time:
# the volume of only sell trades that occurred within 1-minute period.
# the volume of only buy trades that occurred within 1-minute period
# the net volume of buy-sell trades that occurred within 1-minute period


# EDA:

# 1.- Describir estadísticas básicas  , media, median ,variance, sd,sesgo,curtosis, quartiles, conteo , min max,
# outliers.
orderbook_a = (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price'])
orderbook_b = (orderbooks['binance'][list(orderbooks['binance'])[2]])

media = orderbook_a.mean()
median = orderbook_a.median()
variance = orderbook_a.var()
std = orderbook_a.std()
curt = kurtosis(orderbook_a)
count = orderbook_a.count()
max_orderbook = orderbook_a.max()
min_orderbook = orderbook_a.min()

quantiles = (path_orderbooks['bid_price']).describe()

q1 = np.percentile((path_orderbooks['bid_price']), 25)
q3 = np.percentile((path_orderbooks['bid_price']), 75)
# 2.- Atípicos "lado minimo" <= q1-[q3-q1]*1.5 todo precio abajo , seria atípico
lado_minimo = q1 - (q3 - q1) * 1.5
#     Atípicos "lado maximo" >= q3+[q3-q1]*1.5
lado_maximo = q3 + (q3 - q1) * 1.5
# 3.- Serie de tiempo(lineas)

series = publictrades['binance'][list(publictrades['binance'])]['amount']
series.plot()
pyplot.show()

# 4.- Histograma de freq de variables

plt.hist(series, bins=10)
plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
# 5.- Boxplot (con media y mediana)
fig = plt.figure(figsize=(10, 7))

# Creating plot
plt.boxplot(series)

# show plot
plt.show()

# 6.- grafica de velas (OHLC) + volume de trades público

exchange = ccxt.binance()
symbol = 'BTC/USDT'
timeframe = '8h'

timeframe_duration_in_seconds = exchange.parse_timeframe(timeframe)
timeframe_duration_in_milliseconds = timeframe_duration_in_seconds * 1000
ohlcvs = exchange.fetch_ohlcv(symbol, timeframe)
for ohlcv in ohlcvs:
    print([exchange.iso8601(ohlcv[0] + timeframe_duration_in_milliseconds - 1)] + ohlcv[1:])

fig = go.Figure(data=[go.Candlestick(x=ohlcvs[0],
                                     open=ohlcvs[1], high=ohlcvs[2],
                                     low=ohlcvs[3], close=ohlcvs[4])
                      ])

fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()
# variable objetivo(problema de Clasificación)
# signo de cambio del precio a un periodo definido (8 horas)

# EDA II

# Resample data to 4h

df_orderbooks = pd.DataFrame(orderbooks)
orderbook4h = df_orderbooks.resample('4H', ).sum()
orderbook4ha = pd.DataFrame(orderbook_b)
orderbook_c = (orderbook4h['binance'][0])

# Target engineering classification problem sign
ohlc = pd.DataFrame(ohlcvs)
ohlc.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
ohlc['timestamp'] = pd.to_datetime(ohlc['timestamp'])
sign = []
for i in range(497):
    sign1 = ohlc["open"][i + 1] - ohlc["close"][i]
    sign.append(sign1)
for i in range(497):
    if sign[i] <= 0:
        sign[i] = 0
    else:
        sign[i] = 1
print(sign)

# Feature engineering 100 candidate features


# Preprocessing Log, Scale, Standardize (mean, median), Normalize

# Model Training  martingala, maquina de soporte vectorial, red neuronal

# Model Evaluation

# Model Explain-ability por como salió y significado de lo que se obtuvo.
