''' 삼중창 매매 시스템의 두번째 창에서는 첫번째 창의 추세 방향과 역행하는 파도를 파악하는데 오실레이터를 활용
오실레이터는 시장이 하락할때 매수 기회를 제공하고, 시장이 상승할때 매도 기회를 제공한다.
즉, 주봉 추세가 상승하고 있을때 일봉 추세가 하락하면 매수 기회로 본다.'''

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from stockdata_analysis import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('엔씨소프트', '2017-01-01')

ema60 = df.close.ewm(span=60).mean()
ema130 = df.close.ewm(span=130).mean()
macd = ema60 - ema130
signal = macd.ewm(span=45).mean()
macdhist = macd - signal

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
    macdhist=macdhist).dropna()
df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number','open','high','low','close']]

ndays_high = df.high.rolling(window=14, min_periods=1).max()
''' ① 14일동안 최대값을 구한다. min_periods=1을 지정할 경우 14일 기간에 해당하는 데이터가 모두 누적되지 않더라도 최소
    기간인 1일 이상의 데이터만 존재하면 최대값을 구하라는 의미임 '''
ndays_low = df.low.rolling(window=14, min_periods=1).min()
''' ② 14일동안 최소값을 구한다. min_periods=1을 지정할 경우 14일 기간에 해당하는 데이터가 모두 누적되지 않더라도 최소
    기간인 1일 이상의 데이터만 존재하면 최소값을 구하라는 의미임 '''
fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100  # ③ 빠른선 %K 구함
slow_d= fast_k.rolling(window=3).mean()                           # ④ 3일동안 %K의 평균을 구해서 느린선 %D에 저장
df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()             # ⑤ %K와 %D로 데이터프레임을 생성한뒤 결측치 제거거

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - Second Screen (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')

p1 = plt.subplot(2, 1, 2)
plt.grid(True)
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['fast_k'], color='c', label='%K')
plt.plot(df.number, df['slow_d'], color='k', label='%D')
plt.yticks([0, 20, 80, 100])  # y축 눈금을 0, 20, 80 ,100으로 설정하여 스토캐스틱의 기준선을 나타낸다.
plt.legend(loc='best')
plt.show()

''' 130일 지수 이동평균 그래프를 표시하고, 아래는 스토캐스틱 그래프를 표시함
    스토캐스틱에는 빠른 선인 %K와 느린 선인 %D가 있다. %K 대신 느린 %D를 사용할 경우 더 적은 신호를 만들어 내기 때문에 
    그만큼 더 확실한 신호로 볼수 있다.
    매매 시스템의 두번째 창에서는 130일 지수 이동 평균이 상승하고 있을때 스토캐스틱이 30 아래로 내려가면 매수 기회로 보고
    130일 지수 이동 평균이 하락하고 있을때 스토캐스틱이 70위로 올라가면 매도 기회로 보면 된다. '''