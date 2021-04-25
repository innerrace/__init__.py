""" 대신증권 클레온으로 거래하는 프로그램임"""

import os, sys, ctypes
import win32com.client
import pandas as pd
from datetime import datetime
from slacker import Slacker
import time, calendar
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

slack = Slacker('xoxb-1328826168885-1499204785509-AT29qreiAuEEfqRFogQJvxfN')


def dbgout(message):
    """인자로 받은 문자열을 파이썬 셸과 슬랙으로 동시에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message)
    strbuf = datetime.now().strftime('[%m/%d %H:%M:%S] ') + message
    slack.chat.post_message('#etf-algo-trading', strbuf)


def printlog(message, *args):
    """인자로 받은 문자열을 파이썬 셸에 출력한다."""
    print(datetime.now().strftime('[%m/%d %H:%M:%S]'), message, *args)


# 크레온 플러스 공통 OBJECT
cpCodeMgr = win32com.client.Dispatch('CpUtil.CpStockCode')
cpStatus = win32com.client.Dispatch('CpUtil.CpCybos')
cpTradeUtil = win32com.client.Dispatch('CpTrade.CpTdUtil')
cpStock = win32com.client.Dispatch('DsCbo1.StockMst')
cpOhlc = win32com.client.Dispatch('CpSysDib.StockChart')
cpBalance = win32com.client.Dispatch('CpTrade.CpTd6033')
cpCash = win32com.client.Dispatch('CpTrade.CpTdNew5331A')
cpOrder = win32com.client.Dispatch('CpTrade.CpTd0311')


def check_creon_system():
    """크레온 플러스 시스템 연결 상태를 점검한다."""
    # 관리자 권한으로 프로세스 실행 여부
    if not ctypes.windll.shell32.IsUserAnAdmin():
        printlog('check_creon_system() : admin user -> FAILED')
        return False

    # 연결 여부 체크
    if (cpStatus.IsConnect == 0):
        printlog('check_creon_system() : connect to server -> FAILED')
        return False

    # 주문 관련 초기화 - 계좌 관련 코드가 있을 때만 사용
    if (cpTradeUtil.TradeInit(0) != 0):
        printlog('check_creon_system() : init trade -> FAILED')
        return False
    return True


def get_current_price(code):
    """인자로 받은 종목의 현재가, 매수호가, 매도호가를 반환한다."""
    cpStock.SetInputValue(0, code)  # 종목코드에 대한 가격 정보
    cpStock.BlockRequest()
    item = {}
    item['cur_price'] = cpStock.GetHeaderValue(11)  # 현재가
    item['ask'] = cpStock.GetHeaderValue(16)  # 매수호가
    item['bid'] = cpStock.GetHeaderValue(17)  # 매도호가
    return item['cur_price'], item['ask'], item['bid']


def get_ohlc(code, qty):
    """인자로 받은 종목의 OHLC 가격 정보를 qty 개수만큼 반환한다."""
    cpOhlc.SetInputValue(0, code)  # 종목코드
    cpOhlc.SetInputValue(1, ord('2'))  # 1:기간, 2:개수
    cpOhlc.SetInputValue(4, qty)  # 요청개수
    cpOhlc.SetInputValue(5, [0, 2, 3, 4, 5])  # 0:날짜, 2~5:OHLC
    cpOhlc.SetInputValue(6, ord('D'))  # D:일단위
    cpOhlc.SetInputValue(9, ord('1'))  # 0:무수정주가, 1:수정주가
    cpOhlc.BlockRequest()
    count = cpOhlc.GetHeaderValue(3)  # 3:수신개수
    columns = ['open', 'high', 'low', 'close']
    index = []
    rows = []
    for i in range(count):
        index.append(cpOhlc.GetDataValue(0, i))
        rows.append([cpOhlc.GetDataValue(1, i), cpOhlc.GetDataValue(2, i),
                     cpOhlc.GetDataValue(3, i), cpOhlc.GetDataValue(4, i)])
    df = pd.DataFrame(rows, columns=columns, index=index)
    return df


def get_stock_balance(code):
    """인자로 받은 종목의 종목명과 수량을 반환한다."""
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]  # 계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1)  # -1:전체, 1:주식, 2:선물/옵션
    cpBalance.SetInputValue(0, acc)  # 계좌번호
    cpBalance.SetInputValue(1, accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
    cpBalance.SetInputValue(2, 50)  # 요청 건수(최대 50)
    cpBalance.BlockRequest()
    if code == 'ALL':
        dbgout('계좌명: ' + str(cpBalance.GetHeaderValue(0)))
        dbgout('결제잔고수량 : ' + str(cpBalance.GetHeaderValue(1)))
        dbgout('평가금액: ' + str(cpBalance.GetHeaderValue(3)))
        dbgout('평가손익: ' + str(cpBalance.GetHeaderValue(4)))
        dbgout('종목수: ' + str(cpBalance.GetHeaderValue(7)))
    stocks = []
    for i in range(cpBalance.GetHeaderValue(7)):
        stock_code = cpBalance.GetDataValue(12, i)  # 종목코드
        stock_name = cpBalance.GetDataValue(0, i)  # 종목명
        stock_qty = cpBalance.GetDataValue(15, i)  # 수량
        if code == 'ALL':
            dbgout(str(i + 1) + ' ' + stock_code + '(' + stock_name + ')'
                   + ':' + str(stock_qty))
            stocks.append({'code': stock_code, 'name': stock_name,
                           'qty': stock_qty})
        if stock_code == code:
            return stock_name, stock_qty
    if code == 'ALL':
        return stocks
    else:
        stock_name = cpCodeMgr.CodeToName(code)
        return stock_name, 0


def get_current_cash():
    """증거금 100% 주문 가능 금액을 반환한다."""
    cpTradeUtil.TradeInit()
    acc = cpTradeUtil.AccountNumber[0]  # 계좌번호
    accFlag = cpTradeUtil.GoodsList(acc, 1)  # -1:전체, 1:주식, 2:선물/옵션
    cpCash.SetInputValue(0, acc)  # 계좌번호
    cpCash.SetInputValue(1, accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
    cpCash.BlockRequest()
    return cpCash.GetHeaderValue(9)  # 증거금 100% 주문 가능 금액


def get_target_price(code):
    """매수 목표가를 반환한다. 매수목표가는 = 금일시작가격 + (어제최고가 - 어제최저가)*K
    K값은 일반적으로 0.5로 설정하는데 K값이 높을수록 목표가에 도달할 가능성이 낮아지고, 낮으면 목표가에 도달할 가능성은
    높아지므로 매수 타이밍이 하루에 몇번정도 발생하는지를 보고 k값을 조정"""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        ohlc = get_ohlc(code, 10)  # 인수로 받은 종목의 열흘치 OHLC 데이터를 조회
        if str_today == str(ohlc.iloc[0].name):
            # 첫번째 OHLC 행의 인덱스 날짜가 오늘이면 두번째 OHLC 행을 어제의 OHLC 데이터로 사용
            # 첫번째 OHLC 행의 인덱스 날짜가 오늘이 아니면 첫번째 OHLC 행을 어제의 OHLC 데이터로 사용
            today_open = ohlc.iloc[0].open  # 오늘의 시가는 첫번째 OHLC 행의 '시가' 열을 사용
            lastday = ohlc.iloc[1]
        else:
            lastday = ohlc.iloc[0]
            today_open = lastday[3]  # 오늘의 시가가 존재하지 않을 경우 어제의 종가를 대신 사용
        lastday_high = lastday[1]
        lastday_low = lastday[2]
        target_price = today_open + (lastday_high - lastday_low) * 0.5
        # 목표 매수가는 오늘시가 + (어제 최고가 - 어제 최저가) * K 로 계산
        return target_price
    except Exception as ex:
        dbgout("`get_target_price() -> exception! " + str(ex) + "`")
        return None


def get_movingaverage(code, window):
    """변동성 돌파 전략의 매수 조건은 현재가가 (시가 + 전일 변동폭의 K%)를 돌파할때다.
        여기에 현재가가 5일 이동평균선과 10일 이동 평균선 위에 있어야 한다는 조건을 추가함
        특정 종목의 종목코드와 이동평균의 기준일을 인자로 받은 종목에 대한 이동평균가격을 반환하는 함수이다."""
    try:
        time_now = datetime.now()
        str_today = time_now.strftime('%Y%m%d')
        ohlc = get_ohlc(code, 20)
        # 인수로 받은 종목의 한달치 OHLC 데이터를 조회
        if str_today == str(ohlc.iloc[0].name):
            # 첫번째 OHLC 행의 인덱스 날짜가 오늘이면 두번째 OHLC 행의 인덱스 날짜를 어제 날짜로 사용
            # 첫번째 OHLC 행의 인덱스 날짜가 오늘이 아니면 첫번째 OHLC 행의 인덱스 날짜를 어제 날짜로 사용
            lastday = ohlc.iloc[1].name
        else:
            lastday = ohlc.iloc[0].name
        closes = ohlc['close'].sort_index()  # 종가 칼럼을 인데스 날짜 기준으로 오름차순 정렬
        ma = closes.rolling(window=window).mean()  # 종가 칼럼의 이동 평균 구함
        return ma.loc[lastday]  # 어제에 해당하는 날짜 인덱스를 이용하여 이동 평균값으 구한뒤 반환
    except Exception as ex:
        dbgout('get_movingavrg(' + str(window) + ') -> exception! ' + str(ex))
        return None


def buy_etf(code):
    """인자로 받은 종목을 최유리 지정가 FOK 조건으로 매수한다.
        ETF 종목은일반 주식 종목에 비하면 거래량이 그리 많지 않은 경우가 많으므로 한꺼번에 원하는 수량 만큼  매수하려면
        비싼 가격을 지불하는 경우가 발생할수 있다. 이러한 상황을 피하려면 최유리 FOK 매수 주문을 통해 현재 가장 낮은 매도
        호가에 매수 주문을 냄으로써 원하는 가격에 원하는 수량만큼 매수가 가능할때만 계약이 체결 되도록 한다."""
    try:
        global bought_list  # 함수 내에서 값 변경을 하기 위해 global 로 지정
        if code in bought_list:  # 매수 완료 종목이면 더 이상 안 사도록 함수 종료
            # printlog('code:', code, 'in', bought_list)
            return False
        time_now = datetime.now()
        current_price, ask_price, bid_price = get_current_price(code)
        # 인수로 주어진 종목에 대한 현재가, 매수호가, 매도호가를 조회
        target_price = get_target_price(code)  # 매수 목표가
        ma5_price = get_movingaverage(code, 5)  # 5일 이동평균가
        ma10_price = get_movingaverage(code, 10)  # 10일 이동평균가
        buy_qty = 0  # 매수할 수량 초기화
        if ask_price > 0:  # 매수호가가 존재하면
            buy_qty = buy_amount // ask_price
            # 종목별 현금 주문 가능 금액을 매수호가로 나누어 매수할 수량을 정함
        stock_name, stock_qty = get_stock_balance(code)  # 종목명과 보유수량 조회
        # printlog('bought_list:', bought_list, 'len(bought_list):',
        #    len(bought_list), 'target_buy_count:', target_buy_count)
        if current_price > target_price and current_price > ma5_price \
                and current_price > ma10_price:
            # 현재가가 매수 목표가를 돌하하고, 5일 이동평균가와 10일 이동평균가보다 높은 가격에 있다면 매수 조건으로 판단
            printlog(stock_name + '(' + str(code) + ') ' + str(buy_qty) +
                     'EA : ' + str(current_price) + ' meets the buy condition!`')
            cpTradeUtil.TradeInit()
            acc = cpTradeUtil.AccountNumber[0]  # 계좌번호
            accFlag = cpTradeUtil.GoodsList(acc, 1)  # -1:전체,1:주식,2:선물/옵션
            # 최유리 FOK 매수 주문 설정
            cpOrder.SetInputValue(0, "2")  # 2: 매수
            cpOrder.SetInputValue(1, acc)  # 계좌번호
            cpOrder.SetInputValue(2, accFlag[0])  # 상품구분 - 주식 상품 중 첫번째
            cpOrder.SetInputValue(3, code)  # 종목코드
            cpOrder.SetInputValue(4, buy_qty)  # 매수할 수량
            cpOrder.SetInputValue(7, "2")  # 주문조건 0:기본, 1:IOC, 2:FOK
            cpOrder.SetInputValue(8, "12")  # 주문호가 1:보통, 3:시장가
            # 5:조건부, 12:최유리, 13:최우선
            # 매수 주문 요청
            ret = cpOrder.BlockRequest()  # 최유리 지정가 FOK 조건으로 매수 주문을 낸다
            printlog('최유리 FoK 매수 ->', stock_name, code, buy_qty, '->', ret)
            if ret == 4:
                remain_time = cpStatus.LimitRequestRemainTime
                printlog('주의: 연속 주문 제한에 걸림. 대기 시간:', remain_time / 1000)
                time.sleep(remain_time / 1000)  # 잦은 주문으로 연속 주문 제한에 걸리면 제한이 해제될때까지 기다린다.
                return False
            time.sleep(2)
            printlog('현금주문 가능금액 :', buy_amount)
            stock_name, bought_qty = get_stock_balance(code)
            printlog('get_stock_balance :', stock_name, stock_qty)
            if bought_qty > 0:
                bought_list.append(code)
                # FOK 조건으로 매수 주문을 냈으므로 주식이 하나 이상 존재하면 매수가 완료된 것으로 보고 매수 완료 리스트에 해당 종목 추가
                dbgout("`buy_etf(" + str(stock_name) + ' : ' + str(code) +
                       ") -> " + str(bought_qty) + "EA bought!" + "`")
    except Exception as ex:
        dbgout("`buy_etf(" + str(code) + ") -> exception! " + str(ex) + "`")


def sell_all():
    """ 오후 03:15부터 03:20까지 매수한 종목 모두 최유리 지정가 IOC 조건으로 매도한다."""
    try:
        cpTradeUtil.TradeInit()
        acc = cpTradeUtil.AccountNumber[0]  # 계좌번호
        accFlag = cpTradeUtil.GoodsList(acc, 1)  # -1:전체, 1:주식, 2:선물/옵션
        while True:
            stocks = get_stock_balance('ALL')
            # 현재 계좌에 보유한 모든 주식 잔고 조회. stocks 리스트는 종목명, 종목코드, 보유수량 저어보를 딕셔너리 원소로 갖는다.
            total_qty = 0
            for s in stocks:
                total_qty += s['qty']  # stocks 리스트의 주식 종목별 보유수량을 모두 합해서 전체 수량을 구함
            if total_qty == 0:
                return True
            for s in stocks:
                if s['qty'] != 0:  # 보유수량이 존재하는 주식 종목이 남아 있다면 매도 조건으로 본다.
                    cpOrder.SetInputValue(0, "1")  # 1:매도, 2:매수
                    cpOrder.SetInputValue(1, acc)  # 계좌번호
                    cpOrder.SetInputValue(2, accFlag[0])  # 주식상품 중 첫번째
                    cpOrder.SetInputValue(3, s['code'])  # 종목코드
                    cpOrder.SetInputValue(4, s['qty'])  # 매도수량
                    cpOrder.SetInputValue(7, "1")  # 조건 0:기본, 1:IOC, 2:FOK
                    cpOrder.SetInputValue(8, "12")  # 호가 12:최유리, 13:최우선
                    # 최유리 IOC 매도 주문 요청
                    ret = cpOrder.BlockRequest()
                    # 최유리 지정가(IOC) 조건으로 남은 보유 수량 전부 매도, 가능 수량 만큼 체결되고 미체결 수량은 다음 반복시 재매도 주문
                    printlog('최유리 IOC 매도', s['code'], s['name'], s['qty'],
                             '-> cpOrder.BlockRequest() -> returned', ret)
                    if ret == 4:
                        remain_time = cpStatus.LimitRequestRemainTime
                        printlog('주의: 연속 주문 제한, 대기시간:', remain_time / 1000)
                time.sleep(1)
            time.sleep(30)
    except Exception as ex:
        dbgout("sell_all() -> exception! " + str(ex))

# EtfAlgoTrader.py 파일을 모듈로 실행할때만 메인 처리 로직이 동작하도록 if 문을 사용
if __name__ == '__main__':
    """ 앞에서 구현한 함수들을 시간대별로 동작하도록 하는 것이 메인 로직이다.
        symbol_list 에 지정한 매수 후보군 종목들의 현재가를 주기적으로 조회하다가 목표 가격을 돌파하는 종목을 매수해서
        장 마감시 무조건 매도한다. 단일 종목을 매매하는 것보다 여러 종목을 매매하는 것이 리스크 분산에 유리하기 때문에
        본 예제는 목표 종목수를 5개로 설정"""
    try:
        symbol_list = ['A122630', 'A252670', 'A233740', 'A250780', 'A225130',
                       'A280940', 'A261220', 'A217770', 'A295000', 'A176950']
        # 변동성 돌파 전략으로 매수할 ETF 후보 리스트 (시가총액이 크고 거래량이 많은 종목중에서 수익률이 높은 종목으로 선택)
        bought_list = []  # 매수 완료된 종목 리스트
        target_buy_count = 5  # 매수할 종목 수
        buy_percent = 0.19
        """ 하루에 매수할 종목수를 5개로 정했기 때문에 종목별 주문 비율을 20%로 설정하는 것이 맞으나 소득세(15.4%)가 과세되기
            때문에 19%만 매수하고 나머지 금액은 배당소득세를 내는데 쓰일수 있게 남겨둔다. """
        printlog('check_creon_system() :', check_creon_system())  # 크레온 접속 점검
        stocks = get_stock_balance('ALL')  # 보유한 모든 종목 조회
        total_cash = int(get_current_cash())  # 100% 증거금 주문 가능 금액 조회
        buy_amount = total_cash * buy_percent  # 종목별 주문 금액 계산
        printlog('100% 증거금 주문 가능 금액 :', total_cash)
        printlog('종목별 주문 비율 :', buy_percent)
        printlog('종목별 주문 금액 :', buy_amount)
        printlog('시작 시간 :', datetime.now().strftime('%m/%d %H:%M:%S'))
        soldout = False;

        while True:
            t_now = datetime.now()
            t_9 = t_now.replace(hour=9, minute=0, second=0, microsecond=0)
            t_start = t_now.replace(hour=9, minute=5, second=0, microsecond=0)
            t_sell = t_now.replace(hour=15, minute=15, second=0, microsecond=0)
            t_exit = t_now.replace(hour=15, minute=20, second=0, microsecond=0)
            today = datetime.today().weekday()
            if today == 5 or today == 6:  # 토요일이나 일요일이면 자동 종료
                printlog('Today is', 'Saturday.' if today == 5 else 'Sunday.')
                sys.exit(0)
            if t_9 < t_now < t_start and soldout == False:
                soldout = True
                sell_all()
            if t_start < t_now < t_sell:  # AM 09:05 ~ PM 03:15 : 목표가를 돌파하는 종목이 있다면 매수
                for sym in symbol_list:
                    if len(bought_list) < target_buy_count:
                        buy_etf(sym)
                        time.sleep(1)
                if t_now.minute == 30 and 0 <= t_now.second <= 5:
                    get_stock_balance('ALL')
                    time.sleep(5)
            if t_sell < t_now < t_exit:  # PM 03:15 ~ PM 03:20 : 일괄 매도
                if sell_all() == True:
                    dbgout('`sell_all() returned True -> self-destructed!`')
                    sys.exit(0)
            if t_exit < t_now:  # PM 03:20 ~ :프로그램 종료
                dbgout('`self-destructed!`')
                sys.exit(0)
            time.sleep(3)
    except Exception as ex:
        dbgout('`main -> exception! ' + str(ex) + '`')
