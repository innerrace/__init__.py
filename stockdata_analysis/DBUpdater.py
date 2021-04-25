""" 매일 일정한 시간에 네이버 금융데이터를 웹스크레이핑해서 마리아디비에 업데이트하는 DBUpdater 클래스 작성
    실행하기전 def execute_daily(self): 내용 확인 필요 (매일 데이터 업데이트시 설정이 필요함)
    pages_to_fetch = 120 (처음 받고 싶은 데이터 만큼 config.json 파일내에 {"pages_to_fetch": 120} 값을 설정한다.)
    config = {'pages_to_fetch': 1}  # 다 받은 이후에는 1로 수정해주면 당일 자료만 추가로 받아준다

    https://github.com/investar/StockAnalysisInPython 참조할것

    """

import pandas as pd
from bs4 import BeautifulSoup
import urllib
import pymysql
import calendar
import time
import json
import requests
from urllib.request import urlopen
from datetime import datetime
from threading import Timer

'''일반적인 mysql 핸들링 코드 작성 순서
    1. PyMySQl 모듈 import
    2. pymysql.connect() 메소드 사용하여 MySQL 에 연결 (호스트명, 포트, 로그인, 암호, 접속할 DB 등 파라미터 지정)
    3. MySQL 접속이 성공하면 Connection 객체로 부터 cursor() 메서드를 호출하여 Cursor 객체를 가져옴
    4. Cursor 객체의 execute() 메서드를 사용하여 SQL 문장을 DB 서버에 전송
    5. SQL 쿼리의 경우 Cursor 객체의 fetchall(), fetchone(), fetchmany() 등의 메소드를 사용하여 서버로부터
       가져온 데이터를 코드에서 활용
       fetchall(): fetch all the rows
       fetchone(): fetch the next row
       fetchmany(size=None): fetch several rows
    6. 삽입, 갱신, 삭제 등의 DML(Data Manipulation Language) 문장을 실행하는 경우,  INSERT/UPDATE/DELETE 후 Connetion
       객체의 commit() 메서드를 사용하여 데이터를 확정
    7. Connection 객체의 close() 메서드를 사용하여 DB 연결을 닫음   '''


class DBUpdater:

    # DBUpdater 클래스는 객체가 생성될때 마리아디비에 접속하고 소멸될때 접속을 해제한다.
    def __init__(self):
        print("DBUpdater 클래스를 실행합니다.")
        # 생성자: MariaDB 연결 및 종목코드 딕셔너리 생성
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='6123cage', db='investar',
                                    charset='utf8')
        """ Python에서 MySQL에 있는 데이타를 사용하는 일반적인 절차는 다음과 같다. 
            1. PyMySql 모듈을 import 한다
            2. pymysql.connect() 메소드를 사용하여 MySQL에 Connect 한다. 호스트명, 로그인, 암호, 접속할 DB 등을 파라미터로 지정한다.
            3. DB 접속이 성공하면, Connection 객체로부터 cursor() 메서드를 호출하여 Cursor 객체를 가져온다. DB 커서는 Fetch 동작을 
               관리하는데 사용되는데, 만약 DB 자체가 커서를 지원하지 않으면, Python DB API에서 이 커서 동작을 Emulation 하게 된다.
            4. Cursor 객체의 execute() 메서드를 사용하여 SQL 문장을 DB 서버에 보낸다.
            5. SQL 쿼리의 경우 Cursor 객체의 fetchall(), fetchone(), fetchmany() 등의 메서드를 사용하여 데이타를 서버로부터 
               가져온 후, Fetch 된 데이타를 사용한다.
            6. 삽입, 갱신, 삭제 등의 DML(Data Manipulation Language) 문장을 실행하는 경우, INSERT/UPDATE/DELETE 후 Connection 
               객체의 commit() 메서드를 사용하여 데이타를 확정 갱신한다.
            7. Connection 객체의 close() 메서드를 사용하여 DB 연결을 닫는다.
            한글 회사명을 사용하기 때문에 인코딩 오류 발생 할수 있음 connect() 함수 사용할때 미리 utf8 인코딩 형식 지정
            port = 3306 추가함 """

        with self.conn.cursor() as curs:
            # 접속 성공후 cursor object 를 가져와서 curs 로 변환
            # cursor 는 control structure of database 로 (연결된 객체로 봐도 됨)
            sql = """
            CREATE TABLE IF NOT EXISTS company_info (
                code VARCHAR(20),
                company VARCHAR(40),
                last_update DATE,
                PRIMARY KEY (code))
            """
            # 이미 존재하는 테이블에 CREATE TABLE 구문 사용하면 오류 발생 => IF NOT EXISTS 구문을 추가하여 경고 메시지만 표시하고
            # 프로그램은 계속 실행될수 있도록 처리

            curs.execute(sql)  # execute() 메소드로 SQL 실행하기

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
            # SQL 실행하기, curs 객체를 execute() 메서드를 사용하여 삽입,업데이터 및 삭제문장을 DB 서버로 보냄

        self.conn.commit()
        # 삽입,업데이터 및 삭제등이 모드 끝났으면 Connection 객체의 commit() 메서드를 사용하여 데이터를 Commit (저장) 한다.
        self.codes = dict()

        # self.update_comp_info() 원본 코드에 없어서 주석 처리함
        # 생성자가 수행하는 또 다른 기능은 update_comp_info() 메서드로 KRX 주식 코드를 읽어와서 마리아의 company_info 테이블에 업데이트함

    def __del__(self):
        """소멸자: MariaDB 연결 해제"""

        self.conn.close()
        # Connection 객체의 close() 메서드를 사용하여 DB 연결을 닫음

    # 종목코드 구하기 => 한국거래소 사이트에서 제공하는 '상장법인목록.xls 파일' 을
    # 다운로드해 문자열로 변경하는 코드
    def read_krx_code(self):
        """KRX 로부터 상장기업 목록 파일을 읽어와서 데이터프레임으로 반환"""
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13'  # http -> https
        krx = pd.read_html(url, header=0)[0]
        """ 상장법인목록.xls 파일을 read_html()함수로 읽음
        pd.read_html을 이용하면 html에 있는 table속성에 해당하는 값을 가져올 수 있다.
        이는 웹페이지에 있는 표를 불러오겠다는 의미이다.
        pandas.read_html(URL, match='.+', flavor=None, header=None, index_col=None, skiprows=None, attrs=None, 
        parse_dates=False, tupleize_cols=None, thousands=', ', encoding=None, decimal='.', converters=None, 
        na_values=None, keep_default_na=True, displayed_only=True)
        • URL : 대상 url 입력
        • match : str or compiled regular expression, optional
        : 정규표현식 또는 문자열을 이용해서 전체 테이블을 가져오지말고 원하는 내용이 들어있는 테이블만 가져오게 함.
        • flavor = None / ‘bs4’ / ‘html5lib’
        : html을 parsing할 engine 선택. None일 경우 'lxml'으로 시도된 후, 실패하면 bs4 + html5lib으로 수행된다.
        • header = int or list-like or None, optional
        : header로(열 이름) 쓸 행을 지정할 수 있다.
        • encoding = str or None, optional
        : 인코딩 설정. 한글이 깨져서 나올 때 encoding = 'utf-8'으로 설정하면 된다.  """
        krx = krx[['종목코드', '회사명']]
        # 종목 코드외 회사명을 남긴댜. 데이터프레임에 [[]]를 사용하면 특정 칼럼만 뽑아서 원하는 순서대로 재구성할수 있다.
        krx = krx.rename(columns={'종목코드': 'code', '회사명': 'company'})
        # 한글 컬럼명을 영문으로 변경
        krx.code = krx.code.map('{:06d}'.format)
        # 종목코드 형식을 {:06d} 로 변경, format()을 쓰면 튜플변경 불가로 인한 오류가 발생하므로 ()을 지워 객체로서 접근한다.
        return krx

    # company_info 테이블에 last_update 칼럼을 조회하여 오늘 날짜로 업데이트한 기록이 있으면 더는 업데이터 하지 않도록했다.

    def update_comp_info(self):
        """종목코드를 company_info 테이블에 업데이트 한 후 딕셔너리에 저장"""
        sql = "SELECT * FROM company_info"
        df = pd.read_sql(sql, self.conn)
        """ company_info 테이블을 read_sql()함수로 읽음
            DB 에서 취득하고 싶은 내용을 작성한 쿼리를 read_sql()를 사용해 실행하면 결과값을 Dataframe 형태로 얻을 수 있습니다. """
        for idx in range(len(df)):
            self.codes[df['code'].values[idx]] = df['company'].values[idx]
            # 종목코드와 회사명으로 codes 딕셔너리 생성

        with self.conn.cursor() as curs:
            sql = "SELECT max(last_update) FROM company_info"
            curs.execute(sql)
            rs = curs.fetchone()  # fetchone(): fetch the next row
            # SELECT max() 구문 이용 DB 에서 가장 최근 업데이트 날짜 가져옴

            today = datetime.today().strftime('%Y-%m-%d')
            if rs[0] == None or rs[0].strftime('%Y-%m-%d') < today:
                # 위에서 구한 날짜가 존재하지 않거나 오늘보다 오래된 경우에만 업데이트
                krx = self.read_krx_code()
                # KRX 상장기업 목록 파일 읽어서 krx 데이터프레임에 저장
                for idx in range(len(krx)):
                    code = krx.code.values[idx]
                    company = krx.company.values[idx]
                    sql = f"REPLACE INTO company_info (code, company, last" \
                          f"_update) VALUES ('{code}', '{company}', '{today}')"
                    # REPLACE INTO 구문이용 '종목코드,회사명,오늘날짜' 행을 DB에 저장
                    curs.execute(sql)
                    ''' 테이블에 데이터행을 삽입하는데 INSERT INTO 구문을 사용하지만
                    데이터행이 테이블에 이미 존재하면 오류 발생으로 프로그램 종료
                    REPLACE INTO 구문 사용하면 동일한 행이 존재하더라도 오류없이
                    UPDATE 수행'''

                    self.codes[code] = company
                    # codes 딕셔너리에 '키-값' 으로 종목모트돠 회사명 추가
                    tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                    print(f"[{tmnow}] #{idx + 1:04d} REPLACE INTO company_info ", f"VALUES ({code}, {company}, {today})"
                          )
                self.conn.commit()
                print('')  # 원본은 print('')

                # 주식 시세 데이터 읽어오기 (네이버 금융에서 일별 시세 스크레이핑 하는 코드임)

    def read_naver(self, code, company, pages_to_fetch):
        """네이버에서 주식 시세를 읽어서 데이터프레임으로 반환
        네이버 시세페이지를 스크레이핑할때 pgRR 클래스의 <td>태그가 존재
        하지 않으면 AttributeError 가 발생하면서 종료됨
        find() 함수 결과가 None 인 경우에는 다음 종목을 처리하도록 변경"""
        try:
            url = f"http://finance.naver.com/item/sise_day.nhn?code={code}"
            """with urlopen(url) as doc:
                if doc is None:
                    return None
                html = BeautifulSoup(doc, "lxml")
                ''' html 객체가 정상적으로 생성됐는지 확인하기 위해 prettify 메서드를 호출해서 전체 소스를 출력해 볼수 있다.
                    prettify 메소드는 HTML 코드를 콘솔에 보기 좋게 출력하는 역할을 한다.
                    print(html, prettify()) 사용해 볼것
                    html 객체가 정상적으로 생성되면 dot(.)나 []를 이용해서 HTML 요소에 접근할수 있다.'''
                pgrr = html.find("td", class_="pgRR")
                if pgrr is None:
                    return None
                s = str(pgrr.a["href"]).split('=')
                lastpage = s[-1]  # 시세의 마지막 페이지 구함 - 구버전 네이버 크롤러 제한으로 변경"""
            html = BeautifulSoup(requests.get(url,
                                              headers={'User-agent': 'Mozilla/5.0'}).text, "lxml")
            """ 서버에서 봇으로 인지하고 원하는 정보를 주지 않고 차단한 경우
                headers 정보에  User-Agent 를 넣어주면 되는데요. (여기서 헤더(header)는, 접속하는 사람/프로그램에 대한 
                정보를 가지고 있습니다. 정보는 한 가지 항목이 아닌 여러가지 항목이 들어갈 수 있기에  복수형태로 headers 로 입력합니다)
                headers = {'User-Agent' : '유저정보'}
                url = '접속하고픈사이트'
                requests.get(url, headers = headers)
                이렇게 입력을 하면, 나는 '유저정보'란  유저야. 이 사이트에는 어떠한 정보가 있는지 알려줘~ 뭐 이렇게 이야기를 
                하게 되는거죠. 크롤링을 방지하는 사이트에서 만약 User-Agent 를 점검하는 로직이 있다면, 이와 같은 방법으로 해결
            """
            pgrr = html.find("td", class_="pgRR")
            if pgrr is None:
                return None
            s = str(pgrr.a["href"]).split('=')
            """ a 태그(Tag)는 문서를 링크 시키기 위해 사용하는 태그(Tag)
                href 속성은 <a> 태그(Tag)를 통해 연결할 주소를 지정 한다."""

            lastpage = s[-1]
            df = pd.DataFrame()
            pages = min(int(lastpage), pages_to_fetch)
            # 설정파일에 설정된 페이지수(pages_to_fetch)와 시세마지막 페이지수에서 작은것 택함
            for page in range(1, pages + 1):
                pg_url = '{}&page={}'.format(url, page)
                df = df.append(pd.read_html(requests.get(pg_url,
                    headers={'User-agent': 'Mozilla/5.0'}).text)[0])  # 이전 코드 (pg_url, header=0)[0]
                # 일별시세 페이지를 read_html() 함수로 읽어서 데이터프레임에 추가
                tmnow = datetime.now().strftime('%Y-%m-%d %H:%M')
                print('[{}] {} ({}) : {:04d}/{:04d} pages are downloading...'.
                      format(tmnow, company, code, page, pages), end="\r")
            df = df.rename(columns={'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low',
                                    '거래량': 'volume'})
            # 한국 칼럼을 영문 칼럼으로 변경
            df['date'] = df['date'].replace('.', '-')  # 연.월.일 => 연-월-일
            df = df.dropna()
            df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close',
                                                                         'diff', 'open', 'high', 'low',
                                                                         'volume']].astype(int)
            # astype(int)로 마리아디비에서 BIGINT 형으로 지정된 칼럼들의 데이터형을 Int 형으로 변경
            df = df[['date', 'open', 'high', 'low', 'close', 'diff', 'volume']]
            # 원하는 순서로 칼럼을 재조합하여 데이터프레임을 만든다.
        except Exception as e:
            print('Exception occured :', str(e))
            return None
        return df

    # 일별 시세 데이터를 DB에 저장하기

    def replace_into_db(self, df, num, code, company):
        """네이버에서 읽어온 주식 시세를 DB에 저장하는 함수"""
        with self.conn.cursor() as curs:
            for r in df.itertuples():  # 인수로 넘겨받은 데이터프레임을 튜플로 순회처리
                sql = "REPLACE INTO daily_price VALUES ('{}','{}', {},{}, {},{}, {},{})".format(code, r.date, r.open, r.
                                                                                                high, r.low, r.close, r.
                                                                                                diff, r.volume)

                ''' sql = f"REPLACE INTO daily_price VALUES ('{code}', "\
                    f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                    f"{r.diff}, {r.volume})" 원본에는 f 가 있음'''

                # REPLACE INTO 구문으로 daily_price 테이블을 업데이터한다.
                curs.execute(sql)
            self.conn.commit()  # commit()함수 마리아디비에 반영
            print('[{}] #{:04d} {} ({}) : {} rows > REPLACE INTO daily_price [OK]'.format(datetime.now().strftime(
                '%Y-%m-%d' ' %H:%M'), num + 1, company, code, len(df)))

    def update_daily_price(self, pages_to_fetch):
        """KRX 상장법인의 주식 시세를 네이버로부터 읽어서 DB에 업데이트하는 메서드"""
        for idx, code in enumerate(self.codes):
            df = self.read_naver(code, self.codes[code], pages_to_fetch)
            # read_naver() 메서드를 통해 종목코드에 대한 일별 시세 데이터 프레임을 구함
            if df is None:
                continue
            self.replace_into_db(df, idx, code, self.codes[code])
            # 구한 일별 시세를 replace_into_db() 메서드로 DB에 저장

    '''config.json 파일을 이용해 DBUpdater 가 처음 실핻되었는지 여부를 체크
    해당 파일이 없으면 DBUpdater 가 처음 실행하는 경우이므로 네이버 시세 데이터를
    종목별로 100페이지씩 가져온다. 최초 업데이트한 이후부터는 1페이지씩 가져오도록
    자동으로 변경. 업데이터할 페이지수를 변경하려면 config.json 파일내 
    {"pages_to_fetch":1}값을 수정하면 된다.  text 에 {"pages_to_fetch":1}를 입력한후
    config.json 로 저장하면 된다. 100페이지는 4년간 자료로 전종목별로 100페이지를
    읽어오는데 5시간 소요 189MB 용량 차지'''

    def execute_daily(self):
        """execute_daily() 메서드는 DBUpdater.py 모듈의 시작 포인트
        실행 즉시 및 매일 오후 다섯시에 daily_price 테이블 업데이트"""
        self.update_comp_info()  # update_comp_info() 메소드로 상장법인목록 DB 업데이트

        try:
            with open('config.json', 'r') as in_file:
                config = json.load(in_file)
                pages_to_fetch = config['pages_to_fetch']
                # 파일이 있으면 pages_to_fetch 값을 읽어 프로그램에 사용
        except FileNotFoundError:  # 파일이 없는 경우
            with open('config.json', 'w') as out_file:
                pages_to_fetch = 100
                """ <중요> 처음 받고 싶은 데이터 만큼 config.json 파일 열어  {"pages_to_fetch": 100} 값을 설정한다. """
                config = {'pages_to_fetch': 1}  # 다 받은 이후에는 1로 수정해주면 당일 자료만 추가로 받아준다
                json.dump(config, out_file)
        self.update_daily_price(pages_to_fetch)
        # pages_to_fetch 값으로 update_daily_price() 메서드 호출

        tmnow = datetime.now()
        lastday = calendar.monthrange(tmnow.year, tmnow.month)[1]
        # 이번 달의 마지막 날을 구해 다음날 오후 5시를 계산하는데 사용
        if tmnow.month == 12 and tmnow.day == lastday:
            tmnext = tmnow.replace(year=tmnow.year + 1, month=1, day=1,
                                   hour=17, minute=0, second=0)
        elif tmnow.day == lastday:
            tmnext = tmnow.replace(month=tmnow.month + 1, day=1, hour=17,
                                   minute=0, second=0)
        else:
            tmnext = tmnow.replace(day=tmnow.day + 1, hour=17, minute=0,
                                   second=0)
        tmdiff = tmnext - tmnow
        secs = tmdiff.seconds
        t = Timer(secs, self.execute_daily)
        # 다음날 오후 5시에 execute_daily() 메서드를 실행하는 타이머(Timer)객체 생성
        print("Waiting for next update ({}) ... ".format(tmnext.strftime
                                                         ('%Y-%m-%d %H:%M')))
        t.start()


# 매일 일정한 시간에 네이버 금융데이터를 웹스크레이핑해서 마리아디비에 업데이트하는 DBUpdater 클래스 작성

if __name__ == '__main__':
    dbu = DBUpdater()
    # 위 3개의 함수를 모은 것으로 DBUpdater.py가 단독으로 실행되면 DBUpdater 객체를 생성

    dbu.execute_daily()

    ''' company_info 테이블에 오늘 업데이터된 내용이 있는지 확인후 없으면 
        def read_krx_code(self):호출 하여 company_info 테이블에 업데이터 codes 
        딕셔너리에 저장
       윈도우 명령창에서 python C:\\Users\\inner\\Investar\\DBUpdater.py 실행해서 결과 확인
      
      매일 오후5시 정각에 DB를 업데이터하려면 마리아디비 설정 파일에서 wait_timeout
      값을 변경해야 한다. DBUpdater 의 생성자에서 connect() 함수로 마리아디비에 
      연결한뒤 8시간 이상 사용하지 않으면 ConnectionAbortedError(10053)가 발생해
      자동으로 마리아디비와 연결이 종료됨
      NaruaDB 10.5 설치 폴더에 data 안에 my.ini 수정
      파일 내용중 
      innodb_buffer_pool_size=1000M 밑에 wait_timeout=288000 (80시간) 삽입'''

    ''' DBUpdater 배치 파일 만들기 
      윈도우 키 +R 클릭후 실행 창을 띄운후 'regedit' 입력후 레지스트리 편집기 실행
      HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run 키를 마우스 우클릭후
      새로 만들기 메뉴 클릭 => 문자열 값 메뉴를 클릭해서 DBUPDATER 라는 문자열값으로 
      C:\\Users\\inner\\PycharmProjects\\StockAnalysisInPython-master\\Investar\\DBUpdater.bat
      경로를 지정해두면 윈도우 서버가 재시작 되더라도 자동으로 DBUpdater.bat 가 실행되어 최종적으로 DBUpdater.py
      모듈이 실행 된다. '''