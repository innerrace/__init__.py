
""" 변동성 돌파 전략은 가격이 전일 가격 범위의 K% 이상이 될때 매수한 후 장마감 시 매도해서 수익을 실현하는 단기 트레이딩
    기법이다. 추세가 한번 형성되면 가격은 계속 그 방향으로 움직인다는 추세 추종 이론에 기반
    래리 윌리엄스가 개발한 Williams %R 지표는 스토캐스틱에서 파생되었다. 일정기간 동안의 최고가와 최저가 중심축에서
    현재가가 중심축의 어느 위치에 있는지를 %로 표시
    변동성 돌파 전략은 일 단위로 이루어지는 단기 매매법이다.
    매매 기간이 하루를 넘기지 않고 무조건 종가에 매도하기 때문에 장마감 후 악재가 발생하더라도 매매에 영향을 미치지 않아서
    다음날 시가에 매도하는 것보다 상대적으로 더 안전하다
    1) 전날으 고가에서 저가를 빼서 가격 변동폭을 계산
    2) 장중 가격이 오늘 시간 + 전일 변동폭 *K를 돌파할때 매수한다 (일반적으로 K값은 0.5를 사용하지만 수익률에 따라 조정하는 것이 좋다
    3) 장마감 시 무조건 매도한다.

    ETF 는 상장지수펀드라고도 불리며 인덱스 펀드를 거래소에 상장시켜 주식처럼 편리하게 매매할수 있도록 만든 상품이다.
    가장 큰 장점은 주식처럼 거래마다 세금을 내지 않아도 되는점이 주식대신 ETF 로 변동성 돌파를 구현하는 이유다.
    또한 채권처럼 일정 규모 이사의 큰 투자금액이 필요한 자산도 ETF 를 이용하면 소액으로 주자 할수 있다는 장점이 있다.
    국내 모든 ETF 종목의 코드와 시세 정보는 네이버금융>국내증시>주요시세정보>ETF 에서 조회
    1) pip install selenium 설치
    2) 크롬브라우저를 실행한뒤 주소창에 chrome://version 을 입력하여 버전 확인
    3) https://sites.google.com/a/chromium.org/chromedriver/downloads 에서 자신의 크롬 버전에 맞는 웹드라이버를
    다운로드한 후 압축을 풀고 chromedriver.exe 파일을 C:\\Users\\inner\\PycharmProjects\\Investar 에 복사
    4) 탐색기에서 python.exe, idle.exe, chromedriver.exe 파일의 속성창을 열어서 호환성 탭에서 '관리자 권한으로서
       이프로그램 실행 , 체크박스에 체크한다. (관리자 권한으로 설정안해도 현재 코드에서는 작동됨)
    5) 아래 코드와 같이 DynamicPageScraping_NaverETF.py 작성후 실행 """

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

# 옵션값 설정
opt = webdriver.ChromeOptions()
opt.add_argument('headless')

# 웹드라이버를 통해 네이버 금융 ETF 페이지에 접속
drv = webdriver.Chrome('C:\\Users\\inner\\PycharmProjects\\Investar\\chromedriver.exe', options=opt)
drv.implicitly_wait(3)
drv.get('https://finance.naver.com/sise/etf.nhn')

# 뷰티풀 수프로 테이블을 스크래핑
bs = BeautifulSoup(drv.page_source, 'lxml')
drv.quit()
table = bs.find_all("table", class_="type_1 type_etf")
df = pd.read_html(str(table), header=0)[0]

# 불필요한 열과 행을 삭제하고 인덱스를 재설정해서 출력
df = df.drop(columns=['Unnamed: 9'])
df = df.dropna()
df.index = range(1, len(df)+1)
print(df)

# 링크 주소에 포함된 종목코드를 추출하여 전체 종목코드와 종목명 출력
etf_td = bs.find_all("td", class_="ctg")
etfs = {}
# 동적페이지를 스크레이핑하며 전체 330개 ETF 종목코드를 구해서 etfs 딕셔너리를 생성, 향후 자동매매 프로그램에서 전체 ETF 종목에
# 대한 순회 처리를 할때 활용할수 있다.
for td in etf_td:
    s = str(td.a["href"]).split('=')
    code = s[-1]
    etfs[td.a.text] = code
print("etfs :", etfs)

