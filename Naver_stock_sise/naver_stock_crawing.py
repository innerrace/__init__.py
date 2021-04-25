# 참고 https://excelsior-cjh.tistory.com/109 내용임
# 실행시 오류 발생됨

import pandas as pd

code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
# 한국거래소(krx)에서 주식시장에 상장된 기업들 종목 코드 제공. read_html() 함수 이용해서 종목 코드 받아옴
# pd.read_html()는 HTML 에서 <table></table> 태그를 찾아 자동을 DataFrame 형식으로 만들어준다
# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌

code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'company', '종목코드': 'code'})
code_df.head()

print(code_df)

# 특정 종목뿐만 아니라 사용자가 원하는 종목의 일자데이터를 가져올 수 있도록 get_url 이라는 함수를 만들어 줬다
# 각 종목마다 페이지 수가 다르기 때문에 BeautifulSoup 이나 Scrapy 를 이용하여 페이지 수를 크롤링하는 방법이 있지만 20페이지
# 정도만 가져와도 충분하다고 판단하여 별도의 크롤링 없이 20페이지만 가져오도록 지정해줬다.
# 크롤링을 적용하고 싶으면 Python/Web Crawling 을 참고하면 된다.

# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와 네이버 금융(http://finance.naver.com)에 넣어줌


def get_url(item_name, code_df):
    code = code_df.query("name =='{}'".format(item_name))['code'].to_string(index=False)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    print("요청 URL = {}".format(url))
    return url

# 신라젠의 일자데이터 url 가져오기
item_name ='신라젠'
url = get_url(item_name, code_df)

# 일자 데이터를 담을 df라는 DataFrame 정의
df = pd.DataFrame()

# 1페이지에서 20페이지의 데이터만 가져오기
for page in range(1, 21):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

# df.dropna()를 이용해 결측값 있는 행 제거
df = df.dropna()

# 상위 5개 데이터 확인하기
df.head()

print(df)

# 한글로 된 컬럼명을 영어로 바꿔줌
df = df.rename(columns= {'날짜': 'date', '종가': 'close', '전일비': 'diff', '시가': 'open', '고가': 'high', '저가': 'low', '거래량': 'volume'})

# 데이터의 타입을 int형으로 바꿔줌
df[['close', 'diff', 'open', 'high', 'low', 'volume']] = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)

# 컬럼명 'date' 의 타입을 date 로 바꿔줌
df['date'] = pd.to_datetime(df['date'])

# 일자(date)를 기준으로 오름차순 정렬
df = df.sort_values(by=['date'], ascending=True)

# 상위 5개 데이터 확인
df.head()

print(df)

# 필요한 모듈 import 하기 
import plotly.offline as offline 
import plotly.graph_objs as go 

# jupyter notebook 에서 출력 
offline.init_notebook_mode(connected=True) 

trace = go.Scatter( x=df.date, y=df.close, name=item_name) 

data = [trace] 

# data = [celltrion] 
layout = dict( 
            title='{}의 종가(close) Time Series'.format(item_name), 
            xaxis=dict( 
                rangeselector=dict( 
                    buttons=list([ 
                        dict(count=1, 
                            label='1m', 
                            step='month', 
                            stepmode='backward'), 
                        dict(count=3, 
                            label='3m', 
                            step='month', 
                            stepmode='backward'), 
                        dict(count=6, 
                            label='6m', 
                            step='month', 
                            stepmode='backward'), 
                        dict(step='all') 
                    ]) 
                ), 
                rangeslider=dict(), 
                type='date' 
            ) 
        ) 
fig = go.Figure(data=data, layout=layout) 
offline.iplot(fig)
