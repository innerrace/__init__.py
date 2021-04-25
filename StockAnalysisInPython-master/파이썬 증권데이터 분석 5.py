# 야후 파이낸스의 삼성전자 데이터 => 수정종가가 틀리게 표시된다. 2018년 5월초 액면분할을 시행했음에도 액면분할 이전 종가와 수정 종가가 틀리게 표시

from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt

df = pdr.get_data_yahoo('005930.KS', '2017-01-01')  # 삼성전자를 2017-01-01 부터 조회

plt.figure(figsize=(9, 6))
plt.subplot(2, 1, 1)  # 2행1열 영역에서 첫번째 영역 선택
plt.title('Samsung Electronics (Yahoo Finance)')
plt.plot(df.index, df['Close'], 'c', label='Close')  # 종가를 청록색 실선으로 표시
plt.plot(df.index, df['Adj Close'], 'b--', label='Adj Close')  # 수정 종가를 파란색 점선으로 표시
plt.legend(loc='best')
plt.subplot(2, 1, 2)  # 2행1열의 영역에서 두번째 영역 선택
plt.bar(df.index, df['Volume'], color='g', label='Volume')  # 거래량을 바(bar)챠트로 그린다
plt.legend(loc='best')
plt.show()

"""네이버 금융데이터로 시세 데이터베이스 구축
   시세조회 API는 Investar 패키지의 Analyzer 모듈에 포함되어 있는 MarketDB 클래스의 get_daily_price() 메서드다.
   get_daily_price() 메서드를 사용하려면 마리아디비를 설치하고 DBUpdater.py를 이용해 일별 시세 데이터를 업데이터하는 작업을 진행
   아나콘다 파워셀에서 pip3 install pymysql 설치할것. 환경 변수 편집에서 Path 에 C:\\Users\\inner\\Investar 추가 """

from stockdata_analysis import Analyzer
""" Investar 패키지의 Analyzer 모듈 import, Investar 패키지는 실습용 패키지로 pip 로 설치 못함
    Investar 디렉터리 생성후 Analyzer.py, DBUpdater.py, MarketDB.py 파일 복사해 사용 """

mk = Analyzer.MarketDB()  # MarketDB 클래스로부터 mk 객체 생성
df = mk.get_daily_price('005930', '2017-07-10', '2018-06-30')  
""" get_daily_price() 메서드를 사용하려면 마리아디비 설치후 DBUpdater.py를 이용해서 일별 시세 데이터를 업데이트하는 작업을 
    진행해야 한다. (에러발생 원인 추정됨).  조회할 기간 시작, 끝 """
plt.figure(figsize=(9, 6))
plt.subplot(2, 1, 1)
plt.title('Samsung Electronics (Investar Data)')
plt.plot(df.index, df['close'], 'c', label='Close')  # 종가만 청록색으로 표시
plt.legend(loc='best')
plt.subplot(2, 1, 2)
plt.bar(df.index, df['volume'], color='g', label='Volume')
plt.legend(loc='best')
plt.show()

""" MySQL(인터페이스기반 ) 클라이언트 접속 확인. 윈도우 검색창에서 CMD 입력후 도스명령어 창을 들어감

Microsoft Windows [Version 10.0.18363.1139]
(c) 2019 Microsoft Corporation. All rights reserved.

C:\\Users\\inner>cd C:\\Program Files\\MariaDB 10.5\\bin  => 마리아디비설치 장소로 이동

C:\\Program Files\\MariaDB 10.5\\bin>mysql.exe -u root -p  => mysql.exe 실행
Enter password: ********    => password: 설정한 6123cage 입력
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 24
Server version: 10.5.6-MariaDB mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\\h' for help. Type '\\c' to clear the current input statement.

MariaDB [(none)]> CREATE DATABASE Investar;  => Investar명의 데이터베이스 생성
ERROR 1007 (HY000): Can't create database 'investar'; database exists
MariaDB [(none)]> CREATE DATABASE Kiwoom;  
=> 이전에 Investar 명 생성해서 에러 발생하여 Kiwoom 으로 생성
Query OK, 1 row affected (0.007 sec)

MariaDB [(none)]> SHOW DATABASES;  => 생성된 데이터베이스 목록 보여줌
+--------------------+
| Database           |
+--------------------+
| information_schema |
| investar           |
| kiwoom             |  => Kiwoom 생성된 것 보임
| mysql              |
| performance_schema |
| test               |
+--------------------+
6 rows in set (0.013 sec)

MariaDB [(none)]> USE Investar;  => 사용할 데이터베이스를 Investar 로 변경
Database changed
MariaDB [Investar]> SHOW TABLES;  
=> none 에서 Investa r로 변경되었고 Investar 안에 존재하는 테이블 확인
+--------------------+
| Tables_in_investar |
+--------------------+
| company_info       |  => 이전에 만든 테이블 2개 표현, 없으면 empty set 로 표현
| daily_price        |
+--------------------+
2 rows in set (0.001 sec)

MariaDB [Investar]> SELECT VERSION();  => 현재 마리아의 버전 정보 확인
+----------------+
| VERSION()      |
+----------------+
| 10.5.6-MariaDB |
+----------------+
1 row in set (0.001 sec)

MariaDB [Investar]> DROP DATABASE Investar;  => Investar 데이터베이스 제거
ERROR 1010 (HY000): Error dropping database (can't rmdir '.\investar', errno: 41 "Directory not empty")
=> 데이터베이스에 테이블이 있어 제거 되지 않음
MariaDB [Investar]> 

 마리아디비는 오픈소스 관계형 데이터베이스 관리 시스템. 마리아디비는 내부적으로 MySQL 이라는 이름을 사용
    www.mariadb.com 에서 download  (winx64버전) 마이에스큐엘(MySQL)클라이언트 및 헤이디에스큐엘(HeidiSQL:그래픽사용자 인터페이스)
    헤이디에스큐엘이 사용하기 편함.  파이썬내부에서 마리아디비 사용할려면 pip install pymysql 설치
    데이터베이스에서 변경된 내역을 영구적으로 확정하는 것을 커밋(commit)이라고 함
    C:\\Program Files (x86)\\Common Files\\MariaDBShared\\HeidiSQL\\heidisql.exe 실행 """

import pymysql

connection = pymysql.connect(host='localhost', port=3306, db='INVESTAR', 
    user='root', passwd='6123cage', autocommit=True)  
""" 패스워드 지정, connect()함수 호출시 autocommit=Truef 로 설정해주면 별도
    commit() 함수 호출하지 않아도 SQL 문의 실행 결과가 데이터베이스에 반영 """

cursor = connection.cursor()  # cursor()함수 사용 cursor 객체 생성
cursor.execute("SELECT VERSION();")  # execute() 함수로 SELECT 문 실행
result = cursor.fetchone()  # fetchone() 함수를 사용해 실행 결과를 튜플로 받음

print ("MariaDB version : {}".format(result))

connection.close()

""" 주식 시세를 매일 DB로 업데이트 하기
    회사명과 종목코드를 저장한 테이블 만들기 (MySQL 이용)
    MySQL 에서 테이블이 존재하지 않을 경우에만 생성하게 만드려면
    CREATE TABLE IF NOT EXISTS 를 사용하면됨

CREATE TABLE IF NOT EXISTS company_info (
    code VARCHAR(20),
    company VARCHAR(40),
    last_update DATE,
    PRIMARY KEY (code)
);

CREATE TABLE IF NOT EXISTS daily_price (
    code VARCHAR(20),
    date DATE,
    open BIGINT(20),
    high BIGINT(20),
    low BIGINT(20),
    close BIGINT(20),
    diff BIGINT(20),
    volume BIGINT(20),
    PRIMARY KEY (code, date)
);
    헤이디에스뮤엘을 이용해서 쿼리문을 실행하려면 쿼리창을 이용하면 된다.
    데이터베이스명 클릭 => 퉈리탭 클릭 => 실행한 쿼리(코드)입력 => 쿼리실행버튼 클릭 
    쿼리창에 입력된 쿼리문이 실행되면서 데이터베이스에 실제로 테이블이 생성
    위 쿼리문은 데이터를 생성하기 위한 쿼리문임 (단독 실행 안됨)
    매일 일정한 시간에 네이버 금융데이터를 웹스크레이핑해서 마리아디비에 업데이트하는 DBUpdater 클래스 작성 """

import pandas as pd
from bs4 import BeautifulSoup
import urllib, pymysql, calendar, time, json
from urllib.request import urlopen
from datetime import datetime
from threading import Timer

class DBUpdater:
    # DBUpdater 클래스는 객체가 생성될때 마리아디비에 접속하고 소멸될때 접속을 해제한다.

    def __init__(self):
        '''생성자: MariaDB 연결 및 종목코드 딕셔너리 생성'''
        self.conn = pymysql.connect(host='localhost', user='root', password='6123cage', db='investar', charset='utf8')
        # 한글 회사명을 사용하기 때문에 인코딩 오류 발생 할수 있음 connect() 함수 사용할때 미리 utf8 인코딩 형식 지정
        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            # 이미 존재하는 테이블에 CREATE TABLE 구문 사용하면 오류 발생 => IF NOT EXISTS 구문을 추가하여 경고 메시지만 표시하고
            # 프로그램은 계속 실행될수 있도록 처리
            
            curs.execute(sql)
            sql = """
            CREATE TABLE IF NOT EXISTS daily_price (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                diff BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)
            
        self.conn.commit()        
        self.codes = dict()
        
        # self.update_comp_info()
        # 생성자가 수행하는 또 다른 기능은 update_comp_info() 메서드로 KRX 주식 코드를 읽어와서 마리아의 company_info 테이블에 업데이트함
        
    def __del__(self):
        """소멸자: MariaDB 연결 해제"""
        self.conn.close()

# 종목코드 구하기 => 한국거래소 사이트에서 제공하는 '상장법인목록.xls 파일'을 다운로드해 문자열로 변경하는 코드
    def read_krx_code(self):
        """KRX로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=''download&searchType=13'
        krx = pd.read_html(url, header=0)[0]  
        # 상장법인목록.xls 파일을 read_html()함수로 읽음
        krx = krx[['종목코드', '회사명']]
        # 종목 코드외 회사명을 남긴댜. 데이터프레임에 [[]]를 사용하면 특정 칼럼만 
        # 뽑아서 원하는 순서대로 재구성할수 있다.
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        # 한글 컬럼명을 영문으로 변경
        krx.code = krx.code.map('{:06d}'.format) # 종목코드 형식을 {:06d} 로 변경
        return krx
    
# company_info 테이블에 last_update 칼럼을 조회하여 오늘 날짜로 업데이트한 기록이 있으면 더는 업데이터 하지 않도록했다.
    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)  # company_info 테이블을 read_sql()함수로 읽음
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
            # 종목코드와 회사명으로 codes 딕셔너리 생성
                    
        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"            
            curs.execute(sql)
            rs = curs.fetchone()
            # SELECT max() 구문 이용 DB에서 가장 최근 업데이트 날짜 가져옴
            
            today = datetime.today().strftime('%Y-%m-%d')
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                # 위에서 구한 날짜가 존재하지 않거나 오늘보다 오래된 경우에만 업데이트
                krx = self.read_krx_code()
                # KRX 상장기업 목록 파일 읽어서 krx 데이터프레임에 저장
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]                
                    sql = f"REPLACE INTO company_info (code, company, last" f"_update) VALUES ('{code}', '{company}', '{today}')"
                    # REPLACE INTO 구문이용 '종목코드,회사명,오늘날짜' 행을 DB에 저장
                    curs.execute(sql)
                    ''' 테이블에 데이터행을 삽입하는데 INSERT INTO 구문을 사용하지만 데이터행이 테이블에 이미 존재하면 오류 발생으로 프로그램 종료
                        REPLACE INTO 구문 사용하면 동일한 행이 존재하더라도 오류없이 UPDATE 수행'''
                    
                    self.codes[code] = company 
                    # codes 딕셔너리에 '키-값'으로 종목모트돠 회사명 추가
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx+1:04d} REPLACE INTO company_info " f"VALUES ({code}, {company}, {today})")
                self.conn.commit()
                print('')     
                
    # 주식 시세 데이터 읽어오기 (네이버 금융에서 일별 시세 스크레이핑 하는 코드임)
    def read_naver(self, code, company, pages_to_fetch):
        """ 네이버에서 주식 시세를 읽어서 데이터프레임으로 반환
            네이버 시세페이지를 스크레이핑할때 pgRR 클래스의 <td>태그가 존재 하지 않으면 AttributeError가 발생하면서 종료됨
            find() 함수 결과가 None인 경우에는 다음 종목을 처리하도록 변경"""
        try:
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
            with urlopen(url) as doc:
                if doc is None:
                    return None
                html = BeautifulSoup(doc, "lxml")
                pgrr = html.find("td", class_="pgRR")
                if pgrr is None:
                    return None
                s = str(pgrr.a["href"]).split('=')
                lastpage = s[-1] # 시세의 마지막 페이지 구함
            df = pd.DataFrame()
            pages = min(int(lastpage), pages_to_fetch) 
            # 설정파일에 설정된 페이지수(pages_to_fetch)와 시세마지막 
            # 페이지수에서 작은것 택함
            for page in range(1, pages + 1):
                pg_url = '{}&page={}'.format(url, page)
                df = df.append(pd.read_html(pg_url, header=0)[0])
                # 일별시세 페이지를 read_html() 함수로 읽어서 데이터프레임에 추가
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                    format(tmnow, company, code, page, pages), end="\r")
            df = df.rename(columns={'날짜':'date','종가':'close','전일비':'diff'
                ,'시가':'open','고가':'high','저가':'low','거래량':'volume'})
            # 한국 칼럼을 영문 칼럼으로 변경
            df['date'] = df['date'].replace('.', '-') # 연.월.일 => 연-월-일
            df = df.dropna()
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                'diff', 'open', 'high', 'low', 'volume']].astype(int)
            # astype(int)로 마리아디비에서 BIGINT 형으로 지정된 칼럼들의 데이터형을 Int형으로 변경
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
            # 원하는 순서로 칼럼을 재조합하여 데이터프레임을 만든다.
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df
    
    #일별 시세 데이터를 DB에 저장하기
    def replace_into_db(self, df, num, code, company):
        """네이버에서 읽어온 주식 시세를 DB에 저장하는 함수"""
        with self.conn.cursor() as curs:
            for r in df.itertuples(): # 인수로 넘겨받은 데이터프레임을 튜플로 순회처리
                sql = f"REPLACE INTO daily_price VALUES ('{code}', " f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, " \
                      f"{r.diff}, {r.volume})"
                # REPLACE INTO 구문으로 daily_price 테이블을 업데이터한다.
                curs.execute(sql)
            self.conn.commit() # commit()함수 마리아디비에 반영
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_' 'price [OK]'.format(datetime.now().strftime
                                                                                             ('%Y-%m-%d' ' %H:%M'), num+1,
                                                                                             company, code, len(df)))

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트하는 메서드"""  
        for idx, code in enumerate(self.codes):
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            # read_naver() 메서드를 통해 종목코드에 대한 일별 시세 데이터 프레임을 구함
            if df is None:
                continue
            self.replace_into_db(df, idx, code, self.codes[code]) 
            """ 구한 일별 시세를 replace_into_db() 메서드로 DB에 저장
                config.json 파일을 이용해 DBUpdater가 처음 실핻되었는지 여부를 체크. 해당 파일이 없으면 DBUpdater가 처음 실행하는 
                경우이므로 네이버 시세 데이터를 종목별로 100페이지씩 가져온다. 최조 업데이트한 이후부터는 1페이지씩 가져오도록 자동으로 변경. 
                업데이터할 페이지수를 변경하려면 config.json 파일내 {"pages_to_fetch":1}값을 수정하면 된다.  
                text 에 {"pages_to_fetch":1}를 입력한후 config.json 로 저장하면 된다. 100페이지는 4년간 자료로 전종목별로 
                100페이지를 읽어오는데 5시간 소요 189MB 용량 차지 """
 
    def execute_daily(self):
        """ execute_daily() 메서드는 DBUpdater.py 모듈의 시작 포인트 실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트 """
        self.update_comp_info()  # update_comp_info() 메소드로 상장법인목록 DB업데이트
        
        try:
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                pages_to_fetch = config['pages_to_fetch']
                # 파일이 있으면 pages_to_fetch 값을 읽어 프로그램에 사용
        except FileNotFoundError: # 파일이 없는 경우
            with open('config.json', 'w') as out_file:
                pages_to_fetch = 100 # 최초 실행으로 pages_to_fetch 값을 100으로 설정
                config = {'pages_to_fetch': 1}
                json.dump(config, out_file)
        self.update_daily_price(pages_to_fetch) 
        # pages_to_fetch값으로 update_daily_price() 메서드 호출

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        # 이번 달의 마지막 날을 구해 다음날 오후 5시를 계산하는데 사용
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year+1, month=1, day=1, hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month+1, day=1, hour=17, minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day+1, hour=17, minute=0, second=0)
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds
        t = Timer(secs, self.execute_daily)
        # 다음날 오후 5시에 execute_daily() 메서드를 실행하는 타이머(Timer)객체 생성
        print("Waiting for next update ({}) ... ".format(tmnext.strftime('%Y-%m-%d %H:%M')))
        t.start()

# 매일 일정한 시간에 네이버 금융데이터를 웹스크레이핑해서 마리아디비에 업데이트하는 DBUpdater 클래스 작성

if __name__ == '__main__':
    dbu = DBUpdater()  
    # 위 3개의 함수를 모은 것으로 DBUpdater.py가 단독으로 실행되면 DBUpdater 객체를 생성
    dbu.execute_daily()
    ''' company_info 테이블에 오늘 업데이터된 내용이 있는지 확인후 없으면 def read_krx_code(self):호출 하여 company_info 테이블에 
        업데이터 codes 딕셔너리에 저장'''
    # 윈도우 명령창에서 python C:\Users\inner\Investar\DBUpdater.py 실행해서 결과 확인
    # 주식 시세 데이터 읽어오기