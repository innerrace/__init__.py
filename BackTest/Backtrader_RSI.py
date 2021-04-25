""" 백테스트에 사용할 파이썬 라입러리로는 집라인(Zipline), 파이알고트레이드(PyAlgoTrade), 트레이디위드파이썬(Trading With Python)
    파이백테스트(PyBacktest) 등이 있다'. 그중 백트레이더(Backtrader) 라이브러리가 각광을 받는데 문서화가 잘 되어 있고 무엇보다 다른
    라이브러리에 비해 직관적이고 사용하기 편함
    엔시소프트의 상대적 강도 지수(RSI)를 이용해서 매매  수익률을 확인
    RSI 는 금융 시장 분석을 위한 기술적 지표 중의 하나로 가겨의 움직임의 강도를 백분율로 나타내며, 언제 추세가 전환될지 예측하는데 유용
    RS = N 일간의 상승폭 평균 / N 일간의 하락폭 평균
    RSI = 100 - (100 / (1+RS))
    일반적으로 RSI 가 70이상일때 과매수 구간으로 보고 매도 시점으로 해석 반대로 30이하면 과매도 구간으로 보고 매수시점으로 해석 """

from datetime import datetime
import backtrader as bt


class MyStrategy(bt.Strategy):
    # bt.Strategy 클래스를 상속 받아서 MyStrategy 클래스 작성
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.data.close)  # MyStrategy 클래스 생성자에서 RSI 지표로 변수를 지정

    def next(self):
        """ next() 메서드는 주어진 데이터와 지표를 만족시키는 최소 주기마다 자동으로 호출
            시장에 참여하고 있지 않을때 RSI 가 30 미만이면 매수, 시장에 참여하고 있을때 RSI 가 70을 초과하면 매도하도록 구현 """
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()


cerebro = bt.Cerebro()
# Cerebro 클래스는 백트레이더의 핵심 클래스로서 데이터를 취합하고 백테스트 또는 라이브 트레이딩을 실행한두 그 결과를 출력하는 기능 담당
cerebro.addstrategy(MyStrategy)
data = bt.feeds.YahooFinanceData(dataname='036570.KS',  # 야후파이낸스 데이터를 가져왔음
    fromdate=datetime(2017, 1, 1), todate=datetime(2019, 12, 1))
cerebro.adddata(data)
cerebro.broker.setcash(10000000)  # 초기 투자 자금을 천만원으로 설정
cerebro.addsizer(bt.sizers.SizerFix, stake=30)
# 주식 매매 단위는 30주로 설정 , 보유 현금에 비해 매수하려는 주식의 총매수 금액이 크면 매수가 이루어지지 않음

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()  # Cerebro 클래스로 백테스트를 실행
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot()
# 백테스트 결과를 챠트로 출력
