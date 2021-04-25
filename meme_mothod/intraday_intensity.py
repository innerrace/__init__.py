''' 볼린저 밴드를 이용한 반전 매매기법은 주가가 반전하는 지점을 찾아내 매수 또는 매도하는 기법
주자가 하단 밴드를 여러차례 태그하는 과정에서 강세 지표가 발생하면 매수하고, 주가가 상단 밴드를 여러 차례
태그하는 과정에서 약세 지표가 발생하면 매도한다.
매수 : 주가가 하단 밴드 부근에서 W형 패턴을 나타내고 강세 지표가 확증할때 매수 (%b가 0.05보다 작고 일중강도 (II%)가
       0보다 크면 매수
매도 : 상단 밴드 부근에서 일련의 주가가 태그가 일어나며, 약세 지표가 확증할때 매도 (%b가 0.95보다 크고 일중강도 (II%)가
       0보다 작으면 매도
일중강도(II%)는 거래량 지표로 거래범위에서 종가의 위치를 토대로 주식 종목의 자금 흐름을 설명한다.
II는 장이 끝나는 시점에서 트레이더들의 움직임을 나타내는데, 종가가 거래 범위 천정권에서 형성되면 1, 중간에서 형성되면 0,
바닥권에서 형성되면 -1이된다.
21일 기간 동안의 II합을 21일 기간 동안의 거래량 합으로 나누어 표준화한 것이 일중 강도율이다.
일중 강도 = (2 * 종가 -고가 -저가) / (고가 - 저가) * 거래량
일중 강도율 + 일중강도의 21일합 / 거래량의 21일 합 *100 '''

import matplotlib.pyplot as plt
from stockdata_analysis import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('SK하이닉스', '2018-11-01')

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])

df['II'] = (2 * df['close'] - df['high'] - df['low'])/ (df['high'] - df['low']) * df['volume']
# SK하이닉스 종가, 고가, 저가, 거래량을 이용하여 일중 강도 II 구함
df['IIP21'] = df['II'].rolling(window=21).sum()/ df['volume'].rolling(window=21).sum() * 100
# 21일간의 일중 강도 II합을 21일간의 거래량 합으로 나누어 일중 강도율 II% 구함
df = df.dropna()

plt.figure(figsize=(9, 9))
plt.subplot(3, 1, 1)
plt.title('SK Hynix Bollinger Band(20 day, 2 std) - Reversals')
plt.plot(df.index, df['close'], 'b', label='Close')
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')

for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:  # %b가 0.05보다 작고 21일 기준 II%가 0보다 크면
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
        # 첫번째 그래프에 매수 시점을 나타내는 종가 위치에 빨간색 삼각형 표시
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:  # %b가 0.95보다 크고 21일 기준 II%가 0보다 작으면
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
        # 첫번째 그래프에 매도 시점을 나타내는 종가 위치에 파란색 삼각형 표시

plt.legend(loc='best')
plt.subplot(3, 1, 2)
plt.plot(df.index, df['PB'], 'b', label='%b')
plt.grid(True)
plt.legend(loc='best')
plt.subplot(3, 1, 3)  # 3행 1열의 세번째 그리드에 일중 강도율 그린다.

for i in range(0, len(df.close)):
    if df.PB.values[i] < 0.05 and df.IIP21.values[i] > 0:
        plt.plot(df.index.values[i], 0, 'r^')  # 세번째 일중 강도율 그래프에서 매수 시점을 빨간색 삼각형으로 표시
    elif df.PB.values[i] > 0.95 and df.IIP21.values[i] < 0:
        plt.plot(df.index.values[i], 0, 'bv')  # 세번째 일중 강도율 그래프에서 매도 시점을 파란색 삼각형으로 표시

plt.bar(df.index, df['IIP21'], color='g', label='II% 21day')  # 녹색 실선으로 21일 일중 강도율을 표시
plt.grid(True)
plt.legend(loc='best')
plt.show()

'''그려진 챠트중 세번째 챠트는 일중 강도율을 표시한 것으로 기관 블록 거래자의 활동을 추적할 목적으로 만들어진 지표다
존볼린저는 일중 강도율을 볼린저 밴드를 확증하는 도구로 사용, 주가가 하단 볼린저 밴드에 닿을때 일중 강도율이 +이면 매수,
반대로 주가가 상단 볼린저 밴드에 닿을때 일중 강도율이 -이면 매도하라고 조언한다.'''

