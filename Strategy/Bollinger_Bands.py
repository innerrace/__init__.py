''' 투자자들의 보조 지표 이용 팬턴을 분석한 결과 기본보조지표인 이동평균선을 제외하고 가장 많이 설정된 보조 지표는
일목균형표, 볼린저 밴드, 매물대, 상대강도지수(RSI), 이동평균수렴확산(MACD) 순이다.
볼린저밴드는 주가의 변동이 표준 정규분포를 따른다는 가정에서 주가의 위아래에 밴드를 표시함으로써 주가의 상대적인
높낮이를 알려준다. 볼린저 밴드는 주가의 20일 이동평균선을 기준으로 상대적인 고점을 나타내는 상단 밴드와 상대적인 저점을
나타내는 하단 밴드로 구성, 상단 밴드 근처는 상대적인 고점, 하단 밴드 근처는 상대적인 저점임
밴드폭이 좁을수록 주가 변동성이 적고, 밴드폭이 넓을수록 변동성이 크다
상단 볼린저 밴드 = 중간 본린저 밴드 + (2*표준편차)
중간 볼린저 밴드 = 종가의 20일 이동평균
하단 볼린저 밴드 = 중간 볼린저 밴드 -(2*표준편차)'''

import matplotlib.pyplot as plt
from stockdata_analysis import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2019-01-02')  # 날짜 확인 필요

df['MA20'] = df['close'].rolling(window=20).mean()  # 20개 종가를 이용해서 평균을 구함
df['stddev'] = df['close'].rolling(window=20).std()  # 20개 종가를 이용해서 표준편차를 구해 stddev 칼럼에  df 추가
df['upper'] = df['MA20'] + (df['stddev'] * 2)  # 상단 볼린저 밴드 계산
df['lower'] = df['MA20'] - (df['stddev'] * 2)  # 하단 볼리저 밴드 계산
df = df[19:]  # 19번째행까지 NaN 이므로 값이 있는 20번째 행부터 사용

plt.figure(figsize=(9, 5))
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
# x좌표 df.index에 해당하는 종가를 y 좌표로 설정해 파란색(#0000ff) 실선으로 표시
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
# x좌표 df.index에 해당하는 상단 볼린저 밴드값을 y 좌표로 설정해 검은실선(r--) 실선으로 표시
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')  # 상단볼린저 밴드와 하단볼린저 밴드 사이를 회색으로 칠한다.
plt.legend(loc='best')
plt.title('NAVER Bollinger Band (20 day, 2 std)')
plt.show()

''' 통계학에 따르면 평균값에서 +-2*표준편차 이내에 표본값 95.4% 존재하므로 주가가 볼린저 밴드 내부에 존재할 확률도 95.4% 이다'''