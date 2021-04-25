""" Backtrader_RSI는 수수료나 세금 계산이 빠져 있다, 주식 매매 단위도 100으로 고정되어 실제 매매와는 차이가 난다.
    RSI 대신 21일 단순 이동평균에 대한 RSI_SMA를 지표로 사용
    bt.indicators 패키지는 Accdecoscillator, ATR, Bollinger, CCI, Crossover, Deviation, DirectionalMove, DMA, EMA,
    Ichimoku, MACD, Momentum, Sma, Stochastic, Williams, WMA 등 대부분 지표를 이미 모듈로 제공"""

import backtrader as bt
from datetime import datetime

class MyStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=21)

    def notify_order(self, order):
        """ notify_order() 메서드는 주문 상태에 변화가 있을때마다 자동으로 실행. 인수로 주문(order)를 객체로 넘겨 받는다.
            주문 상태는 완료(Completed), 취소(Canceled), 마진(Margin), 거절(Rejected) 등으로 나뉜다. """
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:  # 주문상태가 완료이면 매수인지 매도인지 확인하여 상세 주문 정보 출력
            if order.isbuy():
                self.log(f'BUY  : 주가 {order.executed.price:,.0f}, '
                    f'수량 {order.executed.size:,.0f}, '
                    f'수수료 {order.executed.comm:,.0f}, '        
                    f'자산 {cerebro.broker.getvalue():,.0f}')
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:
                self.log(f'SELL : 주가 {order.executed.price:,.0f}, '
                    f'수량 {order.executed.size:,.0f}, '
                    f'수수료 {order.executed.comm:,.0f}, '
                    f'자산 {cerebro.broker.getvalue():,.0f}')
            self.bar_executed = len(self)
        elif order.status in [order.Canceled]:
            self.log('ORDER CANCELD')
        elif order.status in [order.Margin]:
            self.log('ORDER MARGIN')
        elif order.status in [order.Rejected]:
            self.log('ORDER REJECTED')
        self.order = None

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.order = self.buy()
        else:
            if self.rsi > 70:
                self.order = self.sell()

    def log(self, txt, dt=None):  # log() 메서드는 텍스트 메시지를 인수로 받아서 셀화면에 주문일자와 함께 출력하는 역할한다.
        dt = self.datas[0].datetime.date(0)
        print(f'[{dt.isoformat()}] {txt}')

cerebro = bt.Cerebro()
cerebro.addstrategy(MyStrategy)
data = bt.feeds.YahooFinanceData(dataname='036570.KS',
    fromdate=datetime(2017, 1, 1), todate=datetime(2019, 12, 1))
cerebro.adddata(data)
cerebro.broker.setcash(10000000)
cerebro.broker.setcommission(commission=0.0014)
""" 수수료는 매수나 매도가 발생할때마다 차감된다. 0.25%의 증권 거래세와 0.015% 증권거래수수료로 백트레이더에서는 매도 매수 2번으로 
    총 0.28%의 절반으로 0.0014%로 설정 """
cerebro.addsizer(bt.sizers.PercentSizer, percents=90)
""" 사이즈는 매매 주문을 적용할 주식수를 나타냄, 지정하지 않으면 1이다. PercentSizer 를 사용하면 포트폴리오 자산에 대한 퍼센트로 지정
    100으로 지정하면 수수료를 낼수 없어서 OrderMargin 이 발생하므로, 수수료를 차감한 퍼센트로 지정 """

print(f'Initial Portfolio Value : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.run()
print(f'Final Portfolio Value   : {cerebro.broker.getvalue():,.0f} KRW')
cerebro.plot(style='candlestick')
# 주가 표시할때 캔들 스틱 챠트로 표시
