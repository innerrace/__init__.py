
""" 모멘텀 현상은 행동재무학에서 일컫는 군집행동, 정박효과, 확증편향, 처분효과 등의 행동편향에 의해서 발생
    군집행동 : 다수 그룹의 행동을 따라하는 경향
    정박효과 : 정보를 처음 제공받은 시점에 지나치게 의존하는 경향
    확증 편향 : 본인의 믿음과 반대되는 정보을 무시하는 경향
    처분효과 : 수익이 난 주식을 금방 팔고 , 손해 본 주식을 계속 보유하는 경향
    주식시장에서 모멘텀은 한번 움직이기 시작한 주식 가격이 계속 그 방향으로 나아가려는 성질을 가르킨다.
    """

import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
from stockdata_analysis import Analyzer

''' 듀얼모멘텀 투자느 상대강도가 센 주식 종목들에 투자하는 상대적 모멘텀전략과, 시장이 상승 추세일때만 참여하는 절대적
    모멘텀 전략을 하나로 합친 듀얼 전략이다. 절대 모멘텀으로 추세를 측정하게 되면, 상대 모멘텀만 사용했을 때보다
    MDD 를 줄일수 있고 장기적으로 더 높은 수익률을 달성할수 있다.
    듀얼모멘텀 구조는 간단, 전체 종목토드를 구하는 생성자 함수와 상대 모멘텀을 구하는 함수, 절대모멘텀을 구하는 함수'''


class DualMomentum:
    
    def __init__(self):
        """생성자: KRX 종목코드(codes)를 구하기 위한 MarkgetDB 객체 생성"""
        self.mk = Analyzer.MarketDB()
        
    def get_rltv_momentum(self, start_date, end_date, stock_count):
        # 상대모멘텀을 구함
        """특정 기간 동안 수익률이 제일 높았던 stock_count 개의 종목들 (상대 모멘텀) 아래 인수 설정
            - start_date  : 상대 모멘텀을 구할 시작일자 ('2020-01-01')
            - end_date    : 상대 모멘텀을 구할 종료일자 ('2020-12-31')
            - stock_count : 상대 모멘텀을 구할 종목수 (300)
        """
        connection = pymysql.connect(host='localhost', port=3306,
                                     db='investar', user='root', passwd='6123cage', autocommit=True)
        cursor = connection.cursor()

        # 사용자가 입력한 시작일자를 DB 에서 조회되는 일자로 보정
        sql = f"select max(date) from daily_price where date <= '{start_date}'"
        cursor.execute(sql)
        # daily_price 테이블에서 사용자가 입력한 일자와 같거나 작은 일자를 조회함으로써 실제 거래일을 구함
        result = cursor.fetchone()
        print(result)

        if result[0] is None:
            print("start_date : {} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')
        # DB 에서 조회된 거래일을  %Y-%m-%d 포맷 문자열로 변환해 사용자가 입력한 조회시작 일자 변수에 반영
        # 사용자가 입력한 종료일자를 DB 에서 조회되는 일자로 보정

        sql = f"select max(date) from daily_price where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()

        if result[0] is None:
            print("end_date : {} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        ''' 상대모멘텀은 종목별 수익률을 구하는 것이다. KRX 종목별 수익률을 구해서 2차원 리스트 형태로 추가'''
        rows = []  # 빈리스트를 만든후 나중에 2차원 리스트로 처리
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(self.mk.codes):
            sql = f"select close from daily_price " \
                  f"where code='{code}' and date='{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result is None:
                continue
            old_price = int(result[0])  # start_date 일자에 해당하는 가격(old_price)을 daily_price 테이블로부터 조회
            sql = f"select close from daily_price " \
                  f"where code='{code}' and date='{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result is None:
                continue
            new_price = int(result[0])  # end_date 일자에 해당하는 가격(new_price)을 daily_price 테이브로부터 조회
            returns = (new_price / old_price - 1) * 100  # 해당 종목의 수익률은 구함
            rows.append([code, self.mk.codes[code], old_price, new_price, returns])
            ''' 종목별로 구한 종목코드, 종목명, 구 가격, 신 가격, 수익률을 rows 에 2차원 리스트 형태로 추가
                3~12개월 동안의 강세주들이 이후 동일한 기간 동안에도 강세주다. '''

        # 추가된 2차원 리스트를 상대 모멘텀 데이터프레임으로 변환해서 수익률순으로 출력
        df = pd.DataFrame(rows, columns=columns)  # 데티터 프레임으로 생성한뒤 칼럼 5개만 갖도록 구조를 수정
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)  # 수익률 칼럼 기준으로 내림차순으로 정렬
        df = df.head(stock_count)
        df.index = pd.Index(range(stock_count))  # 상대 모멘텀 데이터프레임의 인덱스를 수익률 순위로 변경
        connection.close()
        print(df)
        print(f"\nRelative momentum ({start_date} ~ {end_date}) : " 
              f"{df['returns'].mean():.2f}% \n")
        return df

    # 절대 모멘텀은 자산의 가치가 상승하고 있을때만 투자하고 그렇지 않을때는 단기 국채를 매수하거나 현금을 보유하는 전략이다.

    def get_abs_momentum(self, rltv_momentum, start_date, end_date):
        # get_abs_momentum()함수 호출시 위에서 구한 상대모멘텀을 인수로 넘겨준다
        """특정 기간 동안 상대 모멘텀에 투자했을 때의 평균 수익률 (절대 모멘텀)
            - rltv_momentum : get_rltv_momentum() 함수의 리턴값 (상대 모멘텀)
            - start_date    : 절대 모멘텀을 구할 매수일 ('2020-01-01')
            - end_date      : 절대 모멘텀을 구할 매도일 ('2020-12-31')
        """
        # 절대 모멘텀을 구하는데 제일 먼저 할 일은 인수로 받은 상대 모멘텀 데이터 프레임 rltv_momentum 에서 종목
        # 칼럼(code)을 추출해 다음 처럼 종목 리스트 stocklist 를 생성하는 것이다.
        stocklist = list(rltv_momentum['code'])
        connection = pymysql.connect(host='localhost', port=3306,
                                     db='investar', user='root', passwd='6123cage', autocommit=True)
        cursor = connection.cursor()

        # 사용자가 입력한 매수일을 DB 에서 조회되는 일자로 변경
        sql = f"select max(date) from daily_price " \
              f"where date <= '{start_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()

        if result[0] is None:
            print("{} -> returned None".format(sql))
            return
        start_date = result[0].strftime('%Y-%m-%d')

        # 사용자가 입력한 매도일을 DB 에서 조회되는 일자로 변경
        sql = f"select max(date) from daily_price " \
              f"where date <= '{end_date}'"
        cursor.execute(sql)
        result = cursor.fetchone()

        if result[0] is None:
            print("{} -> returned None".format(sql))
            return
        end_date = result[0].strftime('%Y-%m-%d')

        # 상대 모멘텀의 종목별 수익률을 구해서 2차원 리스트 형태로 추가
        rows = []
        columns = ['code', 'company', 'old_price', 'new_price', 'returns']
        for _, code in enumerate(stocklist):
            sql = f"select close from daily_price " \
                  f"where code='{code}' and date='{start_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result is None:
                continue
            old_price = int(result[0])
            sql = f"select close from daily_price " \
                  f"where code='{code}' and date='{end_date}'"
            cursor.execute(sql)
            result = cursor.fetchone()

            if result is None:
                continue
            new_price = int(result[0])
            returns = (new_price / old_price - 1) * 100
            rows.append([code, self.mk.codes[code], old_price, new_price,
                         returns])

        # 절대 모멘텀 데이터프레임을 생성한 후 수익률순으로 출력
        df = pd.DataFrame(rows, columns=columns)
        df = df[['code', 'company', 'old_price', 'new_price', 'returns']]
        df = df.sort_values(by='returns', ascending=False)
        connection.close()
        print(df)
        print(f"\nAbasolute momentum ({start_date} ~ {end_date}) : " 
              f"{df['returns'].mean():.2f}%")
        return

    ''' 한국형 듀얼모멘텀 전략 (강환국 역자)
        한국시장에서는 3개월 전략이 훨씬 수익이 좋다. (3개월 조건에 종목수가 적을 수록 수익률이 증가함 - 참고)
        한국 자산만으로 운영하는 전략에는 3개월 듀얼모멘텀을 적용하고, 한국 자산과 해외 자산을 혼합하는 경우에는 12개월 듀얼
        모멘텀을 적용하는 한국형 전략도 고려해볼만하다. 또한 90일 미국 국채를 직접 매수하는 대신 iShares 20 + Year Treasury Bond
        ETF(TLT) 같은 ETF 에 투자할 경우 미국 국채 수익률을 추종하면서 환 헤지까지 할수 있는 한국 투자자만의 장점이 있다.
        '''