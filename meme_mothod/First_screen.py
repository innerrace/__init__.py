''' 알렉산더 엘더의 주식시장에서 살아남는 심리투자 법칙 (이레미디어,2010) 참조
매매를 위한 세가지 요소 3M
정신(Mind) : 시장 노이즈에 휩쓸리지 않도록 해주는 원칙
기법(Mothod) : 시장 지표를 활용해 주기를 분석하고 이를 매매에 활용하는 기법
자금(Money) : 리스크를 거래의 일부로 포함시키는 자금 관리

시장 지표는 3가지
이동평균, MACD 시장의 흐름을 나타내는 지표를 추세 지표라고함.
  -> 시장이 움직일때는 잘 맞지만 횡보할때는 잘못된 신호를 줌
스토캐스틱, RSI 처럼 과거 일정기간의 가격 범위 안에서 현재 가격의 상대적인 위치를 나타내는 지표를 오실레이터라고 함.
  -> 횡보장에서 전환점을 포착하는데 적합하지만 가격보다 앞서 변하는 경향이 있다.
기타 지표들은 강세장과 약세장에 따른 강도를 예측한다.

MACD 히스토그램은 MACD보다 매수와 매도 상태를 더 잘 표현
매수와 매도의 비중 뿐만 아니라 강해지고 있는지 약해지고 있는지 보여줌으로 기술적 분석가에게는 최고의 도구다.
MACD 히스토그램 = MACD선 - 신호선
MACD 히스토그램의 기울기를 확인하는 것은 히스토그램이 중심선(0)위에 있는지 아니면 아래에 있는지 확인 하는 것보다 중요
최고의 매수 신호는 MACD 히스토그램이 중심선 아래에 있고, 기울기가 상향 반전하고 있을때 발생
MACD 히스토그램과 가격과 다이버전스는 일년에 몇번만 일어나며 기술적 분석에서 가장 강력한 신호다.'''

''' 삼중창 매매 시스템은 MACD 히스토그램의 주간 추세가 상승하고 있을때 일간 스토캐스틱에서 매수 신호를 취하도록 설계
    알렉산더 엘더가 개발 
    삼중창 시스템은 추세 추종과 역추세 매매법을 함께 사용, 세단계 창을 거쳐 더 정확한 매매 시점을 찾도록 구성
    트레이더에게 매수, 매도, 관망 세가지중 삼중창 첫번째 창을 이용하면 이중 한 선택지를 제거할수 있다.
    상승추세인지 하락추세인지 판단해 상승추세에서는 매수하거나 관망, 하락 추세에서는 매도 하거나 관망
    첫번째 창은 시장 조류 즉, 장기 챠트를 분석하는 것이다.
    예를 들어 트레이더가 일간챠트를 기준으로 매매한다면 긴 주간 챠트로 추세를 분석하는것이다.'''

# <삼중창 매매 시스템의 첫번째 창>

import pandas as pd
import matplotlib.pyplot as plt
import datetime
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
from stockdata_analysis import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('엔씨소프트', '2017-01-01')


ema60 = df.close.ewm(span=60).mean()   # ① 종가의 12주 지수 이동평균에 해당하는 60일지수 이동평균 구함
ema130 = df.close.ewm(span=130).mean() # ② 종가의 26주 지수 이동평균에 해당하는 130일 지수 이동평균 구함
macd = ema60 - ema130                  # ③ ①-②를 해서 MACD선구함
signal = macd.ewm(span=45).mean()      # ④ 신호선 저장(MACD의 9주 지수 이동평균)
macdhist = macd - signal               # ⑤ MACD 히스토그램 구함 (MACD선-신호선)

df = df.assign(ema130=ema130, ema60=ema60, macd=macd, signal=signal,
    macdhist=macdhist).dropna()
df['number'] = df.index.map(mdates.date2num)  # ⑥ 캔들챠트에서 사용할수 있게 날짜형 인덱스를 숫자형으로 변환
ohlc = df[['number','open','high','low','close']]

plt.figure(figsize=(9, 7))
p1 = plt.subplot(2, 1, 1)
plt.title('Triple Screen Trading - First Screen (NCSOFT)')
plt.grid(True)
candlestick_ohlc(p1, ohlc.values, width=.6, colorup='red',
    colordown='blue')  # ⑦ ohlc 의 숫자형 일자, 시가, 고가, 저가, 종가 값을 이용해서 캔들챠트 그림
p1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.plot(df.number, df['ema130'], color='c', label='EMA130')
plt.legend(loc='best')

p2 = plt.subplot(2, 1, 2)
plt.grid(True)
p2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.bar(df.number, df['macdhist'], color='m', label='MACD-Hist')
plt.plot(df.number, df['macd'], color='b', label='MACD')
plt.plot(df.number, df['signal'], 'g--', label='MACD-Signal')
plt.legend(loc='best')
plt.show()

# 삼중창 매매 시스템의 첫번째 창에서는 EMA 130 그래프가 오르고 있을때에만 시장에 참여한다.