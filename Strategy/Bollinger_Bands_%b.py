''' 주가가 볼린저 밴드 어디에 위치하는지를 나타내는 지표
%b값은 종가가 상단밴드에 걸쳐 있을때 1.0, 중간은 0.5, 하단은 0.0이다. 에를 들어 1.1이면 주가가 상단 밴드보다
밴드폭의 10% 만큼 위에 있다는 의미
%b = (종가 -하단볼린저 밴드)/(상단 볼린저 밴드 - 중간볼린저 밴드)'''

import matplotlib.pyplot as plt
from stockdata_analysis import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2019-01-02')

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
# 기존 볼린저 밴드 코드에서 한줄 추가됨. (종가 -하단볼린저 밴드)/(상단 볼린저 밴드 - 중간볼린저 밴드)를 구해서 %b 칼럼 생성
df = df[19:]

plt.figure(figsize=(9, 8))
plt.subplot(2, 1, 1)  # 기존 볼린저 밴드 챠트를 2행1열의 그리드에서 1열에 배치
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
plt.title('NAVER Bollinger Band(20 day, 2 std)')
plt.legend(loc='best')

plt.subplot(2, 1, 2)  # %b 챠트를 2행 1열의 그리드에서 2열에 배치
plt.plot(df.index, df['PB'], color='b', label='%B')  # x좌표 df.index에 해당하는 %b값을 y좌표로 설정해 파란(b) 실선으로 표시
plt.grid(True)
plt.legend(loc='best')
plt.show()