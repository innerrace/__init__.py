''' 추세 추종은 상승추세에 매수하고 하락추세에 매도하는 기법
매수 : 주가가 상단 밴드에 접근하며, 지표가 강세를 확증할때만 매수 (%b가 0.8보다 크고, MFI(현금흐름지표)가 80보다 클때)
매도 : 주가가 하단 밴드에 접근하며, 지표가 약세를 확증할때만 매도 (%b가 0.2보다 크고, MFI(현금흐름지표)가 20보다 작을때)
중심가격을 사용하면 트레이디이 집중적으로 발생하는 주가 지점을 더 잘 나타낼수 있다.
중심가격이란 일정 기간의 고가, 저가, 종가를 합한뒤에 3으로 나눈값이다. 중심가격에 거래량을 곱한 값이 바로 현금 흐름이다.
다른 지표들이 보통 가격 한가지만 분석하는데 반해 MFI(현금흐름지표)는 가격과 거래량을 동시에 분석하므로 상대적으로 신뢰도가
더 높다. 거래량 지표들은 일반적으로 주가에 선행한다는 특징이 있다. MFI는 거래량 데이터에 상대강도지수 개념을 도입한 지표다.
MFI는 상승일 동안의 현금 흐름의 합과 하락일 동안의 현금흐름의 합을 이용
MFI = 100 - (100 / (1+(긍정적 현금흐름/부정적 현금 흐름)))
긍정적 현금 흐름 : 중심가격이 전일보다 상승한 날들의 현금 흐름의 합
부정적 현금 흐름 : 중심가격이 전일보다 하락한 날들의 현금 흐름의 합'''

import matplotlib.pyplot as plt
from stockdata_analysis import Analyzer

mk = Analyzer.MarketDB()
df = mk.get_daily_price('NAVER', '2019-01-02')

df['MA20'] = df['close'].rolling(window=20).mean()
df['stddev'] = df['close'].rolling(window=20).std()
df['upper'] = df['MA20'] + (df['stddev'] * 2)
df['lower'] = df['MA20'] - (df['stddev'] * 2)
df['PB'] = (df['close'] - df['lower']) / (df['upper'] - df['lower'])
df['TP'] = (df['high'] + df['low'] + df['close']) / 3  # 중심가격 구함
df['PMF'] = 0
df['NMF'] = 0
for i in range(len(df.close) - 1):  # 마지막값을 포함하지 않으므로 0부터 종가개수 -2까지 반복
    if df.TP.values[i] < df.TP.values[i + 1]:
        # i번째 중심가격 보다 i+1번째 중심 가격이 높으면
        df.PMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
        # i+1번째 중심 가격과 i+1 번째 거래량의 곱을  i+1번째 긍정적 현금 흐름 PMF (positive money flow) 저장
        df.NMF.values[i + 1] = 0
        # i+1번째 부정적 현금 흐름 NMF(negative money flow) 값은 0으로 저장
    else:
        df.NMF.values[i + 1] = df.TP.values[i + 1] * df.volume.values[i + 1]
        df.PMF.values[i + 1] = 0
df['MFR'] = (df.PMF.rolling(window=10).sum() /
             df.NMF.rolling(window=10).sum())
# 10일 동안의 긍정적 현금 흐름의 합을 10일 동안 부정적 현금 흐름의 합으로 나눈 결과를 현금흐름 비율 MFR(money flow ratio) 칼럼에 저장
df['MFI10'] = 100 - 100 / (1 + df['MFR'])
# 10일 기준으로 현금흐름 지수를 계산한 결과를 MF10(money flow index 10) 칼럼에 저장
# MFI는 0에서 100까지 움직이는 한계 지표로 80을 상회하면 아주 강력한 매수 신호, 20을 하회하면 아주 강력한 매도 신호를 나타냄
df = df[19:]

plt.figure(figsize=(9, 8))
plt.subplot(2, 1, 1)
plt.title('NAVER Bollinger Band(20 day, 2 std) - Trend Following')
plt.plot(df.index, df['close'], color='#0000ff', label='Close')
plt.plot(df.index, df['upper'], 'r--', label='Upper band')
plt.plot(df.index, df['MA20'], 'k--', label='Moving average 20')
plt.plot(df.index, df['lower'], 'c--', label='Lower band')
plt.fill_between(df.index, df['upper'], df['lower'], color='0.9')
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:  # %b가 0.8보다 크고 10일 기준 MFI가 80보다 크면
        plt.plot(df.index.values[i], df.close.values[i], 'r^')
        # 매수 시점을 나타내기 위해 첫번째 그래프의 종가 위치에 빨간색 삼각형 표시함
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:  # %b가 0.2보다 작고 10일 기준 MFI가 20보다 작으면
        plt.plot(df.index.values[i], df.close.values[i], 'bv')
        # 매도 시점을 나타내기 위해 첫번째 그래프의 종가 위치에 파란색 삼각형 표시함
plt.legend(loc='best')

plt.subplot(2, 1, 2)
plt.plot(df.index, df['PB'] * 100, 'b', label='%B x 100')
# MFI 와 비교할수 있게 %b를 그대로 표시하지 않고 100을 곱해서 푸른색 실선으로 표시
plt.plot(df.index, df['MFI10'], 'g--', label='MFI(10 day)')  # 10일 기준으로 MFI를 녹색의 점선으로 표시
plt.yticks([-20, 0, 20, 40, 60, 80, 100, 120])  # Y축 눈금을 -20부터 120까지 20단위로 표시
for i in range(len(df.close)):
    if df.PB.values[i] > 0.8 and df.MFI10.values[i] > 80:
        plt.plot(df.index.values[i], 0, 'r^')
    elif df.PB.values[i] < 0.2 and df.MFI10.values[i] < 20:
        plt.plot(df.index.values[i], 0, 'bv')
plt.grid(True)
plt.legend(loc='best')
plt.show();