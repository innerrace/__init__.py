''' 세번째 창은 챠트나 지표를 필요로 하지 않는다. 첫번째 창과 두번째 창이 동시에 매매 신호를 냈을때 진입 시점을 찾아내는 기법
주간 추세가 상승하면 추적매수 스톱 기법을 사용해 가격 변동에 따라 주문 수준을 수정한다.
하락 추세에서는 추적 매도 스톱 기법을 사용해 가격 변동에 따라 주문 수준을 수정해간다.
주간 추세가 상승하고 있을때 일간 오실레이터가 하락하면서 매수 신호가 발생하면 전일 고점보다 한틱 위에서 매수 주문을 낸다.
이를 추적 매수 스톱이라고 한다. 만약 주간 추세대로 가격이 계속 상승해 전일 고점을 돌파하는 순간 매수 주문이 체결될 것이다.
매수 주문이 체결되면 전일의 저가나 그 전일의 저가 중 낮은 가격보다 한틱 아래에 매도 주문을 걸어 놓음으로써 손실을 막을수 있다.
만약 가격이 하락한다면 매수 스톱은 체결되지 않을것이다. 매수 주문이 체결되지 않으면 다시 전일 고점 1틱 위까지 매수 주문의 수준을
낮추도록 한다. 주간 추세가 반대 방향으로 움직이거나 매수 신호가 취소될때까지 매일 매수 스톱을 낮추면서 주문을 걸어놓는다.

주간 추세    일간오실레이터      행동           주문
상승         상승              관망
상승         하락              매수        추적매수스톱
하락         하락              관망
하락         상승              매도        추적매도스톱'''

''' 필자는 두번째 창에 일간 오실레이트로 스토캐스틱 %D를 사용 했으며 기준 포인트도 70, 30 대신 80, 20 을 사용해 더 확실한 
    신호를 잡아내도록 했다. 즉, 130일 이동 지수평균이 상승하고 %D가 20 아래로 떨어질때 매수하고 130일 이동 지수평균이 하락하고
    %D가 80위로 올라갈때 매도하도록 구현했다.
    중요한 것은 자신의 전략대로 매매를 했을때 어느 정도의 승률로 수익을 낼수 있는냐는 것이다.'''

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
df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal, macdhist=macdhist).dropna()

df['number'] = df.index.map(mdates.date2num)
ohlc = df[['number','open','high','low','close']]

ndays_high = df.high.rolling(window=14, min_periods=1).max()
ndays_low = df.low.rolling(window=14, min_periods=1).min()

fast_k = (df.close - ndays_low) / (ndays_high - ndays_low) * 100
slow_d = fast_k.rolling(window=3).mean()
df = df.assign(fast_k=fast_k, slow_d=slow_d).dropna()

plt.figure(figsize=(9, 9))
p1 = plt.subplot(3, 1, 1)
plt.title('Triple Screen Trading (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red', colordown='blue')
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
for i in range(1, len(df.close)):
    if df.ema130.values[i-1] < df.ema130.values[i] and df.slow_d.values[i-1] >= 20 and df.slow_d.values[i] < 20:
        # 130일 이동 지수평균이 상승하고 %D가 20 아래로 떨어지면
        plt.plot(df.number.values[i], 250000, 'r^')
        # 빨간색 삼각형으로 매수 신호 표시
    elif df.ema130.values[i-1] > df.ema130.values[i] and df.slow_d.values[i-1] <= 80 and df.slow_d.values[i] > 80:
        # 130일 이동 지수평균이 하락하고 %D가 80 위로 상승하면
        plt.plot(df.number.values[i], 250000, 'bv')
        # 파란색 삼각형으로 매수 신호를 표시
plt.legend(loc='best')

p2 = plt.subplot(3, 1, 2)
plt.grid(True)
p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
plt.plot(df.number, df['macd'], color='b', label='MACD')
plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
plt.legend(loc='best')

p3 = plt.subplot(3, 1, 3)
plt.grid(True)
p3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['fast_k'], color='c', label='%K')
plt.plot(df.number, df['slow_d'], color='k', label='%D')
plt.yticks([0, 20, 80, 100])
plt.legend(loc='best')
plt.show()