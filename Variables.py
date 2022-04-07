
publictrades['binance'].keys()
orderbooks['binance'].keys()
list(orderbooks['binance'])[0]
type(list(orderbooks['binance'])[0])

orderbooks['binance'][list(orderbooks['binance'])[2]]
# spread ask price - bid price

spread = orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_price'][0] - orderbooks[
    'binance'][list(orderbooks['binance'])[2]]['bid_price'][0]
spread*10000 # puntos base

# spread , midprice (promedio entre ask y bid)
midprice = (orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_price'][0] + orderbooks[
    'binance'][list(orderbooks['binance'])[2]]['bid_price'][0])*.05

# weighted midprice como midprice pero multiplicados por los volumenes
weighted_midprice = ((orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_price'][0])*(orderbooks[
    'binance'][list(orderbooks['binance'])[2]]['ask_vol'][0]) + (
    (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price'][0])*(orderbooks['binance'][
    list(orderbooks['binance'])[2]]['bid_vol'][0])))*.05


# volumen total bid volume y ask volume, se suman para el total
total_bid_volume = (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_vol']).sum()
total_ask_volume = (orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_vol']).sum()
total_bid_volume-total_ask_volume
# Microprice vol ask / total volume precio medio ponderado por el volumen
orderbookinbalance = total_ask_volume/(total_bid_volume+total_ask_volume)
microprice = midprice*orderbookinbalance
# volume weighted avarage price (VWAP) cada precio se multiplica por el volumen y se divide entre el volumen total
priceask = (orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_price'])
pricebid = (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price'])
volumeask = (orderbooks['binance'][list(orderbooks['binance'])[2]]['ask_vol'])
volumebid = (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_vol'])

vwap_bid=[]
for i in range(100):
    vwap_bid1=(pricebid[i]*volumebid[i])/total_bid_volume
    vwap_bid.append(vwap_bid1)


vwap_ask=[]
for i in range(100):
    vwap_ask1=(priceask[i]*volumeask[i])/total_ask_volume
    vwap_ask.append(vwap_ask1)
imb_dif= total_bid_volume-total_ask_volume
# statics , spread midprice, weighted mid price , total volume, bid volume, ask volume
# dinamycs diff midprice( diferencia entre dos mid prices), midprice return valor final - valor inicial, sign(midprice return)
# 2nd order variance (midprice return)

# tradeflow, volumeflow

# volume per unit of time:
# the volume of only sell trades that ocurred within 1 minute period.
# the volume of only buy trades that ocurred within 1 minute period
#the net volume of buy-sell trades that ocurred within 1 minute period

from scipy.stats import kurtosis
# EDA:

# 1.- Describir estadisticas basica , media, median ,variance, sd,sesgo,curtosis, quartiles, conteo , min max, outliers.
orderbook_a=(orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price'])
orderbook_b=(orderbooks['binance'][list(orderbooks['binance'])[2]])

media = orderbook_a.mean()
median = orderbook_a.median()
variance = orderbook_a.var()
std = orderbook_a.std()
curt = kurtosis(orderbook_a)
count = orderbook_a.count()
max = orderbook_a.max()
min = orderbook_a.min()

quantiles= (orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price']).describe()

q1= np.percentile((orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price']),25)
q3= np.percentile((orderbooks['binance'][list(orderbooks['binance'])[2]]['bid_price']),75)
# 2.- Atipicos "lado minimo" <= q1-[q3-q1]*1.5 todo precio abajo , seria atipico
lado_minimo=q1-(q3-q1)*1.5
#     Atipicos "lado Maximo" >= q3+[q3-q1]*1.5
lado_maximo= q3+(q3-q1)*1.5
# 3.- Serie de tiempo(lineas)

from matplotlib import pyplot
series = publictrades['binance'][list(publictrades['binance'])]['amount']
series.plot()
pyplot.show()

# 4.- Histograma de freq de variables
import matplotlib.pyplot as plt
plt.hist(series,bins=10)
plt.gca().set(title= 'Frequency Histogram',ylabel='Frecuency')
# 5.- Boxplot (con media y mediana)
fig = plt.figure(figsize=(10, 7))

# Creating plot
plt.boxplot(series)

# show plot
plt.show()

# 6.- grafica de velas (OHLC) + volume de trades publicos
import ccxt
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
# variable objetivo(problema de clasificacion)
# signo de cambio del precio a un periodo definido (8 horas)

# EDA II

# Resample data to 4h

df_orderbooks= pd.DataFrame(orderbooks)
orderbook4h= df_orderbooks.resample('4H',).sum()
orderbook4ha=pd.DataFrame(orderbook_b)
orderbook_c=(orderbook4h['binance'][0])


# Target engineering classification problem sign
ohlc= pd.DataFrame(ohlcvs)
ohlc.columns=['timestamp','open','high','low','close','volume']
ohlc['timestamp'] = pd.to_datetime(ohlc['timestamp'])
sign=[]
for i in range(497):
    sign1=ohlc["open"][i+1]-ohlc["close"][i]
    sign.append(sign1)
for i in range(497):
    if sign[i] <= 0:sign[i]=0
    else: sign[i] = 1
print(sign)
# Feature engineering 100 candidate features




# Preprocessing Log, Scale, Standardize (mean, median), Normalize
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


# Model Training  martingala, maquina de soporte vectorial, red neuronal

# Model Evaluation

# Model Explain-ability por como salio y significado de lo que se obtuvo.

