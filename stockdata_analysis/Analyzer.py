import pandas as pd
import pymysql
from datetime import datetime
from datetime import timedelta
import re  # 정규식 사용

# 사용자로부터 종목과 조회기간을 입력 받아 해당 종목의 시세정보를 조회하는 코드다
# get_daily_price() 메서드는 내부적으로 시세정보를 마리아 디비에서 가져오므로 미리 DBUpdater.py를 실행해서 네이버 금융데이터를
# 마리아디비에 업데이트 해두어야 한다.


class MarketDB:
    def __init__(self):
        """생성자: MariaDB 연결 및 종목코드 딕셔너리 생성"""
        print('Market 클래스가 실행됩니다.')
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='6123cage', db='investar',
                                    charset='utf8')
        # 마리아 디비에 접속해서 인스턴스멤버인 conn 객체 생성
        self.codes = {}  # self.codes = dict()
        # 인스턴스 멤버로 codes 딕셔너리 생성
        self.get_comp_info()
        # get_comp_info() 함수 이용해서 company_info 테이블을 읽어와서 codes 에 저장

    def __del__(self):
        """소멸자: MariaDB 연결 해제
        소멸자 함수는 객체가 삭제되는 시점에서 실행, 사용자가 mk=MarketDB()로 객체를 생성했다면 del mk로 명시적으로 객체를
        삭제해야 마리아디비와 연결이 해제됨"""
        self.conn.close()

    # MarketDB 에서 중요한 부분은 get_daily_price() 함수이고 아래코드가 핵심임
    def get_comp_info(self):
        """company_info 테이블에서 읽어와서 codes 에 저장"""
        sql = "SELECT * FROM company_info"
        krx = pd.read_sql(sql, self.conn)
        for idx in range(len(krx)):
            self.codes[krx['code'].values[idx]] = krx['company'].values[idx]

    def get_daily_price(self, code, start_date=None, end_date=None):
        """KRX 종목의 일별 시세를 데이터프레임 형태로 반환
            - code       : KRX 종목코드('005930') 또는 상장기업명('삼성전자')
            - start_date : 조회 시작일('2020-01-01'), 미입력 시 1년 전 오늘
            - end_date   : 조회 종료일('2020-12-31'), 미입력 시 오늘 날짜
          인수= None 형식이면 인수값이 주어지지 않았을때 기본값으로 처리  daily_price 테이블에서 읽어와서 데이터프레임으로 반환
          """
        sql = "SELECT * FROM daily_price WHERE code = '{}' and date >= '{}' and date <= '{}'".format(code, start_date,
                                                                                                     end_date)
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        # read_sql() 함수를 이용해서 SELECT 결과를 데이터프레밍르로 가져오면 정수형 인덱스가 별도 생성
        # 따라서 df.index = df['date']로 데이터 프레임의 인덱스를 date 칼럼으로 새로 설정

        # 조회 시작일과 종료일을 인수로 넘겨주지 않을때 기본 인수값으로 처리하는 함수
        if start_date is None:  # 만일 조회 시작일로 넘겨 받은 인수가 None 이면 인수가 입력되지않은 경우임
            one_year_ago = datetime.today() - timedelta(days=365)  # 1년전 오늘날짜로 %Y-%m-%d 형식으로 처리
            start_date = one_year_ago.strftime('%Y-%m-%d')
            print("start_date is initialized to '{}'".format(start_date))
        else:  # 입력하는 형식이 다양해도 (2020-8-30,2020-08-30,2020.8.30 emd) 세숫자를 분리하면 어떤 형식을 입력해도 처리가능
            start_lst = re.split('\D+', start_date)
            # 정규표현식 '\D+' 로 분리하면 연,월,일에 해당하는 숫자만 남게된다. \D는 숫자가 아닌 문자를 나타냄
            if start_lst[0] == '':
                start_lst = start_lst[1:]
            start_year = int(start_lst[0])
            start_month = int(start_lst[1])
            start_day = int(start_lst[2])
            if start_year < 1900 or start_year > 2200:
                print(f"ValueError: start_year({start_year:d}) is wrong.")
                return
            if start_month < 1 or start_month > 12:
                print(f"ValueError: start_month({start_month:d}) is wrong.")
                return
            if start_day < 1 or start_day > 31:
                print(f"ValueError: start_day({start_day:d}) is wrong.")
                return
            start_date = f"{start_year:04d}-{start_month:02d}-{start_day:02d}"

        if end_date is None:
            end_date = datetime.today().strftime('%Y-%m-%d')
            print("end_date is initialized to '{}'".format(end_date))
        else:
            end_lst = re.split('\D+', end_date)
            if end_lst[0] == '':
                end_lst = end_lst[1:]
            end_year = int(end_lst[0])
            end_month = int(end_lst[1])
            end_day = int(end_lst[2])
            if end_year < 1800 or end_year > 2200:
                print(f"ValueError: end_year({end_year:d}) is wrong.")
                return
            if end_month < 1 or end_month > 12:
                print(f"ValueError: end_month({end_month:d}) is wrong.")
                return
            if end_day < 1 or end_day > 31:
                print(f"ValueError: end_day({end_day:d}) is wrong.")
                return
            end_date = f"{end_year:04d}-{end_month:02d}-{end_day:02d}"

        codes_keys = list(self.codes.keys())
        codes_values = list(self.codes.values())

        if code in codes_keys:
            pass
        elif code in codes_values:
            idx = codes_values.index(code)
            code = codes_keys[idx]
        else:
            print(f"ValueError: Code({code}) doesn't exist.")

        sql = f"SELECT * FROM daily_price WHERE code = '{code}'" f" and date >= '{start_date}' and date <= '{end_date}'"
        df = pd.read_sql(sql, self.conn)
        df.index = df['date']
        return df