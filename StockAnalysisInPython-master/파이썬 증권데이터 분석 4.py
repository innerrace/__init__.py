""" 상장법인 목록 일기
    한국거래소 기업공시채널(kind.krx.co.kr)에 접속 상장법인상세정보>상장법인목로 이동후 excel 버튼 눌러 상장법인 목록 내려받자
    내려받은 파일은 엑셀 파일이나 text에서 열어보면 html 형식이므로 팬더스의 read_excel() 함수로는 읽을수 없다.
    read_html() 함수를 이용해서 파일을 읽어야 한다. read_excel()로 열려면 엑셀로 열어 .xlsx 확장자로 저장하면 사용 가능 """

import pandas as pd
krx_list = pd.read_html('C:\\Users\\inner\\상장법인목록.xls') 
# (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape 발생으로 \를 추가 해줌

krx_list[0]
krx_list[0]['종목코드'] = krx_list[0]['종목코드'].map('{:06d}'.format)
# 종목 코드를 6자리 고정위해 map()함수 사용
krx_list[0]

""" URL을 이용해 인터넷 상 파일도 읽어온다. read_html()함수 이용
    판다스는 다양한 형태의 외부 파일을 읽어와서 데이터프레임의로 변환하는 함수 제공
    CSV read_csv 로 읽고 to_csv 로 쓴다. JSON read_json 로 읽고 to_json 으로 쓴다. HTML read_html 로 읽고 to_html 로 쓴다.
    EXCEL read_excel 로 읽고 to_excel 로 쓴다.  저장시 sheet_name 옵션을 다르게 입력하여 저장하는 sheet를 지정가능
    SQL read_sql 로 읽고 t0_sql 로 쓴다.    형식 pandas.read_csv("파일경로(이름)")
    - 함수의 옵션 1) path 파일의 위치(파일명 포함), URL
                2) header 열이름의 사용될 행의 번호 (기본갑은 0), header 가 없고 첫행부터 데이터가 있는 경우 None 으로 지정 가능
                3) index_col 행인덱스로 사용할 열의 번호 또는 이름
                4) names 열이르믕로 사용할 문자열의 리스트
                5) encoding 텍스트 인코딩 종류를 지정 (예: 'utf-8')"""

df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13')[0]
# read_html() 함수 뒤에 [0]을 붙임으로써 결과값을 테이터 프레임으로 받는다. 밑에 코드와 나누어 결과 확인함

df['종목코드'] = df['종목코드'].map('{:06d}'.format)
df = df.sort_values(by = '종목코드') 
# 오름차순으로 정렬, 내림차순 정렬은 ascendind = False를 넣어주면 된다.

""" 뷰티풀수프는 HTML. XML페이지부터 데이터를 추출하는 파이썬 아리브러리 웹크롤러나 웹스크레이퍼라고 불리는데 크롤은 웹에 링크된 페이지들을 
    따라 돌아다니며 웹사이트의 테이터들을 읽어온다는 의미, 스크레이퍼는 크롤링해서 모은 데이터에서 원하는 정보를 추출한다는 의미. 
    뷰티풀수프는 웹스크레이퍼임. HTML 페이지를 분석할때 네가지 인기 파서 라이브러리 골라서 쓸수 있다.
    그중 'lxml' 속도가 매우 빠르고 유연한 파싱이 가능하다. 뷰티플수프에서 제일 중요한 함수는 원하는 태그를 찾아주는 find_all(), find()
    이다. find_all() 함수는 조건에 맞는 모든 태그를 찾는다. limit=1 인수를 줘서 찾는 숫자 지정 가능. 
    못찾으면 빈리스트 반환, find() 는 None 반환 """

# 네이버 금융에서 셀트리온의 맨 뒤페이지 숫자를 구함. 일자별 시세는 페이지가 많음
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')
    # 첫번째 인수 HTML/XML 페이지의 파일경로나 URL, 두번째 인수는 웹피이지 파싱할 방식
    pgrr = html.find('td', class_='pgRR')
    # class속성이 pgRR 인 td 태그를 찾아 'bs4.element.tag' 타입으로 pgrr 변수에 반환
    # pgRR (Page Right Right) 맨마지막 페이지 의미함
    # class_ 로 표시하는 이유는 파이썬에 class 지시어가 존재하기 때문에 구분하기 위함
    print(pgrr.a['href'])
    # pgrr 밑에 a태그의 href 속성값을 아래와 같이 얻을수 있다. 마지막 페이지 = 계속 늘어나면서 바뀜

print(pgrr.prettify())
# prettify()함수를 이용하면 pgrr의 getTest 속성값을 계층적으로 출력해줌
print(pgrr.text)
# 태그를 제외한 텍스트 부분만 구할때는 text 속성을 이용

with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml')
    # 첫번째 인수 HTML/XML 페이지의 파일경로나 URL, 두번째 인수는 웹피이지 파싱할 방식
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')  # =를 기준으로 분리해서 리스트에 저장
    # s는 ['item/sise_day.nhn?code','068270&page', '378']
    last_page = s[-1]  # s 리스트의 뒷쪽 첫번째
    
df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'

for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)  # 첫번째 {}에 sise_url 들어가고 두번째 {}에 page값 들어감
    df = df.append(pd.read_html(page_url, header = 0)[0])  # 일별시세는 데이블 형태데이터이므로 팬더스의 read_html()함수로 불러옴
    
df = df.dropna()  # 값이 빠진 행을 제거
print(df)

from matplotlib import pyplot as plt

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml') 
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]  

df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'  
for page in range(1, int(last_page)+1):
    page_url = '{}&page={}'.format(sise_url, page)  
    df = df.append(pd.read_html(page_url, header=0)[0])

df = df.dropna()
df = df.iloc[0:30]  # 데이터가 많아 30개만 가져와서 그래프 그림
df = df.sort_values(by='날짜') 

plt.title('Celltrion (close)')
plt.xticks(rotation=45)  # 날짜가 겹쳐 보이므로 90도로 회전해서 표시
plt.plot(df['날짜'], df['종가'], 'co-')  # co 좌표를 청록색 원으로, -는 각 좌표를 실선으로 연결
plt.grid(color='gray', linestyle='--')
plt.show()

''' 캔들챠트를 그릴려면 엠피엘파이낸스 (mplfinance) 패키지를 사용한다.
    pip install --upgrade mplfinance을 아나콘다 파워셀에서 install 해야한다.'''

# 셀트리온 캔들 챠트 그리기 

import mplfinance as mpf

url = 'https://finance.naver.com/item/sise_day.nhn?code=068270&page=1'
with urlopen(url) as doc:
    html = BeautifulSoup(doc, 'lxml') 
    pgrr = html.find('td', class_='pgRR')
    s = str(pgrr.a['href']).split('=')
    last_page = s[-1]  

df = pd.DataFrame()
sise_url = 'https://finance.naver.com/item/sise_day.nhn?code=068270'  
for page in range(1, int(last_page)+1): 
    page_url = '{}&page={}'.format(sise_url, page)  
    df = df.append(pd.read_html(page_url, header=0)[0])

df = df.dropna()
df = df.iloc[0:30]  # 30행만 슬라이싱

df = df.rename(columns={'날짜':'Date', '시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
# 한글 칼럼명을 영문 칼럼명으로 변경
df = df.sort_values(by='Date')  # 날짜 기준 오름차순 정렬
df.index = pd.to_datetime(df.Date)  # data 칼럼을 datetimeindex 형으로 변경한후 인덱스로 설정
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]  # 좌측 5개값만 갖도록 데이터 프레림 구조 변경

mpf.plot(df, title='Celltrion candle chart', type='candle')  # type를 지정하지 않으면 기본으로 'ohlc' 으로 출력됨
mpf.plot(df, title='Celltrion ohlc chart', type='ohlc')

kwargs = dict(title='Celltrion customized chart', type='candle', mav=(2, 4, 6), volume=True, ylabel='ohlc candles')
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
# up='r', down='b' 상승은 삘긴섹. 히릭은 파란색으로 지정 , 관련 색상은 이에 따름
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, **kwargs, style=s)