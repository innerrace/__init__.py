'''시총 1위에서 4위까지 종목으로 포트폴리오 구성후 효율적 투자선을 구함- 5장에서 개발한 MarketDB클래스 일별 시세조회 API를 사용'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stockdata_analysis import Analyzer

mk = Analyzer.MarketDB()
stocks = ['삼성전자', 'SK하이닉스', '현대자동차', 'NAVER']
df = pd.DataFrame()
for s in stocks:
    df[s] = mk.get_daily_price(s, '2016-01-04', '2018-04-27')['close']

daily_ret = df.pct_change()
# 수익률을 비교하려면 종가 대신 일간 변동률로 비교해야 하기 때문에 pct_change()함수 사용해서 일간 변동률을 구한다.
annual_ret = daily_ret.mean() * 252  # 일간 변동률에 평균갑세 252를 곱해서 연간 수익률을 구함 (252는 미국의 1년 평균 개장일)
daily_cov = daily_ret.cov()  # 일간 리스크는 cov() 함수를 이용하여 일간 변동률의 공분산 구함
annual_cov = daily_cov * 252  # 년간 공분산을 구함

port_ret = []
port_risk = []  # 시총 상위 4종목 비중을 다르게 해 포트폴리오 20,000개 생성, 포트폴리오 수익률,리스크,종목 비중을 저장할 각 리스트 생성
port_weights = []

# 몬테카를로 시뮬레이션 : 매우 많은 난수를 이용해 함수의 값을 확률적으로 계산하는 것
# 몬테카를로 시뮬레이션을 이용하여 포트폴리오 20,000개를 생상한 후 각각의 포트폴리오별 수익률, 리스크, 종목비중을 데이터프레임으로
# 구하는 코드임
for _ in range(20000):  # 포트폴리오 20,000개 생성 반복횟수를 사용할일이 없으면 관습적으로 _변수에 할당
    weights = np.random.random(len(stocks))
    # random() 함수를 이용해 포트폴리오 20,000개를 4종목 비중이 다르게 했다. 4개의 랜덤 숫자로 구성된 배열을 생성
    weights /= np.sum(weights)  # 램덤 숫자를 램덤 숫자의 총합으로 나눠 4종목 비중의 합이 1이 되도록 조정

    returns = np.dot(weights, annual_ret)
    # 랜덤하게 생성한 종목별 비중 배열과 종목별 연간 수익률을 곱해 해당 포트폴리오 전체 수익률(returns)을 구한다
    risk = np.sqrt(np.dot(weights.T, np.dot(annual_cov, weights)))

    port_ret.append(returns)  # 포트폴리오 수익률, 리스크, 종목별 비중을 각각의 리스트에 추가
    port_risk.append(risk)
    port_weights.append(weights)

portfolio = {'Returns': port_ret, 'Risk': port_risk}
for i, s in enumerate(stocks):
    portfolio[s] = [weight[i] for weight in port_weights]  # portfolio 딕셔너리에 비중값을 추가
df = pd.DataFrame(portfolio)
df = df[['Returns', 'Risk'] + [s for s in stocks]]
# 최종 생성된 df 데이터프레임을 출력하면, 시총 상위 4 종목의 보유 비율에 따라 포트폴리오 20,000개가 각기 다른 리스크와
# 예상 수익률을 가지는 것을 확인

df.plot.scatter(x='Risk', y='Returns', figsize=(8, 6), grid=True)
plt.title('Efficient Frontier')
plt.xlabel('Risk')
plt.ylabel('Expected Returns')
plt.show() # df 데이터 프레임을 산점도로 출력.  x축 해당 포트폴리오의 리스크, y축은 예상 수익률
''' 산점도는 시가 총액 4종목에 투자 한다고 가정하고 각 종목의 비율을 임으로 정해 포트폴리오 20,000개를 만들어 산점도로 표시
그림에서 파란색 점들이 나이키 상표처럼 곡선으로 이어져 보이는 부분이 효율적 투자선이며, 주어진 리스크에 최대 수익을 나타내는
포트폴리오 집합이다. 상기 종목에 투자할 경우 효율적 투자선 위의 포트폴리오의 비율에 맞추어 4종목에 분산 투자하는 것이 가장 
효율적인 투자 방법임을 의미'''