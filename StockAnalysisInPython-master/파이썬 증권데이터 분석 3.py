import numpy as np
'''넘파이는 파이썬으로 수치 해석이나 동계 관련 작업을 구현할때 가장 기본인
된ㄴ 모듈, ndarray라는 고성능 다차원 배열 개체와 이를 다루는 여러함수 제공'''

A = np.array([[1,2],[3,4]])
'''리스트를 인수로 받아서 배열을 생성하는 array() 함수를 제공 , 2차원 배열생성'''
type(A)  # ndarray 타입 클래스

A.ndim  # 배열의 차원 나타냄
A.shape  # 속성과 각 차원의 배열 크기를 튜플로 나타냄
A.dtype  # 원소 자료형

print(A.max(), A.mean(), A.min(), A.sum())
# 넘파이 배열 객체는 원소별 최대값, 평균값, 최소값, 합계를 구하는 함수도 제공

A[0]  # 배열의 각 요소에 접근하는데는 대괄호 사용, 리스트와 같이 인덱싱, 슬라이싱 가능
A[1]

print(A[0][0], A[0][1])  # prtnt(A[0,0], A[0,1])의 표현도 위 값과 동일

A[A>1]  # 조건에 맞는 원소들만 인덱싱 하는 방법, 대괄호에 조건 표기

'''전치란 배열의 요소 위치를 주대각선 기준으로 뒤바꾸어 주는것 T 속성이나 transpose() 함수 사용'''

A.T  # T 속성을 통해 배열 변경
A.flatten()  # 다차원 함수를 1차원 배열 형태로 변경- 평탄화한다고 표현

# 배열의 연산
A+A
A-A
A*A
A/A

'''넘파이에서는 행력이 크기가 달라도 연산할수 있게 크기가 작은 행렬을 확장해주는데 이것을 브로드캐스팅이라고 함'''
B = np.array([10,100])

A*B

''' pandas는 넘파이를 기반으로 구현되기 때문에 대부분 함수가 넘파이와 유사 시리즈는 1차원 벡터 형태의 자료형이며, 리스트, 튜플 등의 
    시퀀스를 생성자의 인수로 받을수 있다. 시리즈로 생성할 데이터를 리스트 형태로 Series() 생성자에 넘겨주는 것으로 시리즈 생성'''

import pandas as pd  # pandas 라이브러리를 pd로 정함
s = pd.Series([0.0, 3.6, 2.0, 5.8, 4.2, 8.0])
""" 판다스 Series 함수를 이용해서 출력시 인덱스가 자동 생성 0 ~ 5 정수형 위치 인덱스는 대괄호([])안에 위치를 나타내는 숫자를 입력하는 반면 
    인덱스 이름(라벨)를 이용할때는 대괄호([])안에 이름과 함께 따옴표(큰따옴표("") 또는 작은 따옴표(''))를입력한다.
    여러개의 원소를 선택할때는 인덱스의 범위를 지정한다.  
    예) (판다스시리즈변수명[1:2]) 또는 (판다스시리즈변수명[시작인덱스이름: 끝인덱스이름])"""

s.index = pd.Index([0.0, 1.2, 1.8, 3.0, 3.6, 4.8]) # Index()함수로 인덱스 변경
s.index .name = 'MY_IDX'  # 위에 출력된 자료의 인덱스명 설정됨
s.name = 'My_SERIES'  # 위에 출력된 자료의 시리즈명 설정됨

''' 시리즈에 값 추가 방법
1) 인덱스 레이블과 인덱스에 해당하는 값을 한번에 지정
2) append() 메서드로 추가'''

s[5.9] = 5.5

ser = pd.Series([6.7, 4.2], index=[6.8, 8.0])  # 새로운 시리즈 생성
s = s.append(ser)  # 기존 시리즈에 새로운 시리즈 추가

# 데이터 인데싱 방벙은 index 및 values 속성을 사용
s.index[-1]
s.values[-1]
# 실제 가리키는 작업을 수행하는 인덱서를 사용해서 데이터 표시
s.loc[8.0]  # 인덱서값을 사용해서 데이터 표시
s.iloc[-1]  # 정수 순서를 사용해서 데이터 표시

''' iloc와 values는 인덱스 순서에 해당하는 데이터를 출력한다는 점에서 동일하지만 values는 결과값이 복수개일때 배열로 반환하고, 
    iloc는 시리즈로 반환 차이점 있다'''
s.values[:]
s.iloc[:]

s.drop(8.0)  # 시리즈의 원소 삭제시 drop() 메서드 사용, 원소의 인덱스값 넘겨줌
'''출력값에는 마지막 데이터 값이 보이지 않지만 실제로 s 시리즈에는 변화가 없다. 만일 마지막 원소를 삭제한 결과를 s시리즈에도 반영하려면 
    s = sdrop(8.0)로 입력'''

# 시리즈 객체 정보 확인 describe() 함수 사용, 원소개수, 평균, 표준편차, 최소값, 제1사분위수, 제2사분위수, 제3사분위수, 최대값
s.describe()

'''시리즈 인덱스값을 X값, 데이터값을 Y값을 생각해 보면 시리즈는 2차원 데이터 값을 시작화하는 최적의 자료형이다. 맷플립립을 사용 plot() 
    함수 사용'''

import matplotlib.pyplot as plt
plt.title("ELLIOTT_WAVE")
plt.plot(s, 'bs--')  # 시리즈를 bs--(푸른 사각형과 점선) 형태로 출력
plt.xticks(s.index)  # X축의 눈금값을 s 시리즈의 인덱스값으로 설정 
plt.yticks(s.values)  # y축의 눈금값을 s 시리즈의 데이터값으로 설정
plt.grid(True)  # 그래프내 눈금선을 표시해줌
plt.show()

'''팬더스 라이브러리를 이용해서 HTML파일,엑셀파일, 데이터베이스로부터 데이터를 읽어와 데이터프레임 형태로 가공하고 반대로 데이터를 데이터 
    프레임으로 가공후 엑셀 파일, HTML파일, 데이터베이스 등으로 저장
    데이터프레임을 생성할때 별도로 인덱스를 지정하지 않으면 0부터 시작하는 정수 인덱스가 자동으로 생성'''

import pandas as pd
df = pd.DataFrame({'KOSPI':[1915, 1961, 2026, 2467, 2041],'KOSDAQ':[542, 682, 631, 798, 675]})
""" dict로 데이터프레임 만들기
    KOSPI 시리즈와 KOSDAQ 시리즈를 합쳐 데이터프레임을 만듬. 인데스 지정이 없으니, 자동으로 0~4까지 지정"""

df = pd.DataFrame({'KOSPI':[1915, 1961, 2026, 2467, 2041],'KOSDAQ':[542, 682, 631, 798, 675]}, index=[2014, 2015, 2016, 2017, 2018])
""" 인덱스를 지정하기 위해서는 위 항목처럼 index=[지정하고자 하는 인덱스명 표시] 해주면 됨
    칼럼도 columns=[지정하고자 하는 칼럼명 표시] 하면 됨
    - 행인덱스 변경 : DataFrame 객체.index = 새로운 행 인덱스 배열, 열이름 변경   : DataFrame 객체.columns = 새로운 행 인덱스 배열
    위와 같이 .index 과 .columns 속성 사용
    - rename() 메소드를 적용하면 행 인덱스 또는 열이름의 일부를 선택해서 변경 가능 (단 원본 객체르 수정하는 것이 아니라 새로운 데이터
    프레임 객체를 반환한는 것임-원본 객체 변경시 inplace=True 옵션을 설정한다.)
    - 행인덱스 변경 : DataFrame 객체.rename(index={기존인덱스:새인덱스, ... })
    - 열이름 변경   : DataFrame 객체.rename(columns={기존이름:새이름, ... })    
    행또는 열을 삭제하는 명령 drop() 메소드 사용
    행을 삭제할때는 축(axis) 옵션을 axis = 0을 입력하거나, 별도로 입력하지 않는다.
    반면 axis = 1 을 입력하면 열을 삭제한다. 동시에 여려 개의 행 또는 열을 삭제하려면 리스트 형태로 입력
    기존 객체를 변경하지 않고 새로운 객체를 반환함, 변경시 inplace=True 옵션을 설정한다.
    - 행삭제 : DataFrame 객체.drop(행 인덱스 또는 배열, axis=0)
    - 열삭제 : DataFrame 객체.drop(일 이름 또는 배열, axis=1)"""

# 데이터프레임 객체에 포함된 데이터의 전체적인 모습 확인 describd() 메서드 사용
df.describe()
df.info()
""" 데이터 프레임의 크기 확인 시 .shape() 메서드 사용, .describe() 메서드는 산술(숫자) 데이터를 갖는 열에 대한 주요 기술 통계정보 
    요약 출력
    info() 메서드로 데이터프레임 클래스유형, 인덱스정보, 칼럼정보, 메모리 사용량 확인
    info() 메서드는 각 열의 데이터 개수 정보를 출력하지만 반환해주는 값이 없다. count() 메서드는 각열이 가지고 있는 데이터 개수를 
    시리즈 객체로 반환 """

# 각각의 시리즈를 이용한 데이터프레임 생성
kospi = pd.Series([1915, 1961, 2026, 2467, 2041], index = [2014, 2015, 2016, 2017, 2018], name = 'KOSPI')
kosdaq = pd.Series([542, 682, 631, 798, 675], index = [2014, 2015, 2016, 2017, 2018], name = 'KOSDAQ')

df = pd.DataFrame({kospi.name : kospi, kosdaq.name : kosdaq})

columns = ['KOSPI', 'KOSDAQ']  # 리스트를 이용하여 한행씩 추가해서 데이터프레임 생성
index = [2014, 2015, 2016, 2017, 2018]
rows =[]
# 빈 리스트 만들기
rows.append([1915, 542])  # 'KOSPI', 'KOSDAQ'값 추가
rows.append([1961, 682])
rows.append([2026, 631])
rows.append([2467, 798])
rows.append([2041, 675])
df = pd.DataFrame(rows, columns=columns, index=index)

for i in df.index:
    print(i, df['KOSPI'][i], df['KOSDAQ'][i])

# itertuples() 메서드는 데이터프레임의 각 행을 이름있는 튜플 형태로 반환
for row in df.itertuples(name = 'KRX'):
    print(row)

for row in df.itertuples():
    print(row[0],row[1],row[2])

''' iterrows() 메서드는 데이터프레임의 각 행을 인덱스와 시리즈로 조합으로 반환 속도는 itertuples() 메서드가 빠름'''
for idx, row in df.iterrows():
    print(idx, row[0],row[1])

# pip install yfinance 및 pip install pandas_datareader 설치되어 있어야 함
from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()  
# pdr_override() 와 get_data_yahoo() 함수 사용으로 데이터 다운로드

sec = pdr.get_data_yahoo('005930.ks',start='2018-05-04')
# 국내 주식은 6자리 종목코드 뒤에 .KS 및 .KQ를 붙인다
msft = pdr.get_data_yahoo('MSFT',start='2018-05-04')
''' 미국은 심볼 또는 ticker라고 불리는 알파벳 사용 www.nasdaq.com/screening/cimpany-list.aspx에서 미국 상장주식
    전체 회사 리스트와 주식 심볼 확인 가능'''

print(sec, msft)

sec.head(10) 
''' 데이터프레임의 맨 앞 10행 출력 (다운로드 상태 확인). 인수 없으면 5개 출력.  Adj Close는 수정 종가(액면 분할등으로 주식 가격 변동이 
    있을 경우 가격 변동. 이전에 거래된 가격을 현재 주식 가격에 맞춰 수정하여 표시하는 가격)'''

tmp_msft= msft.drop(columns='Volume')  # 위 데이터프레임에서 거래량 칼럼을 제거
tmp_msft.tail()  # tail() 메서드로 데이터프레이미의 제일 뒤 5행을 출력

sec.index  # 데이터프레임 구성 상태 확인

sec.columns  # 데이터프레임 칼럼들에 대한 정보는 cloumns 속성으로 확인

# 종가들에 대한 그래프 출력 및 비교
sec = pdr.get_data_yahoo('005930.KS',start='2018-05-04')
msft = pdr.get_data_yahoo('MSFT',start='2018-05-04')

plt.plot(sec.index, sec.Close, 'b', label = 'Samsung Electronics')
''' X좌표는 날짜 인덱스, Y축은 종가데이터, 마커형태는 푸른색 실선, 범례 표시 레이블은 Samsung Electronics '''
plt.plot(msft.index, msft.Close, 'r--', label='Microsoft')
plt.legend(loc='best')  # 범례 위치를 best로 지정하면 그래프가 표시되지 않는 부분에 표시
plt.show()

'''일간 변동율 주가 비교.  오늘 변동률 = ((오늘종가-어제종가)/어제종가)*100 '''

type(sec['Close'])
sec['Close']
sec['Close'].shift(1)  # shift()함수를 이용해서 데이터를 이동 (인수) 만큼 행이동함
sec_dpc = (sec['Close']/sec['Close'].shift(1)-1)*100
sec_dpc.head()

""" 데이터프레임의 행 데이터를 선택하기 위해서는 loc와 iloc 인덱서를 사용 
    인덱스 이름을 기준으로 행을 선택할때는 loc 이용, 정수형 위치 인데스를 사용할대는 iloc 을 이용
    - loc 탐색대상: 인데스 이름 예) ['a':'c'] → 'a','b','c'
    - iloc 탐색대상: 정수형 위치 인덱스 예) [3:7] → 3, 4, 5, 6 (7제외)
    첫번째 일간 변동율 값이 NaN인데 향후 계산을 위해 NaN을 0으로 변경
    열데이터를 1개 선택할때 대괄호([])안에 열 이름을 따옴표와 함께 입력하거나 도트(.) 다음에 열 이름을 입력하는 두가지 방식이 있다.
    두번째 방법은 반드시 열이름이 문자열일 경우에만 가능하다.
    - 열 1개 선택(시리즈생성) : DataFrame 객체["열이름"] 또는 DataFrame 객체.열이름  
    - 열 n 선택(데이터프레임 생성) : DataFrame 객체[[열1, 열2, ..., 열n] 
    데이터 프레임의 행인덱스와 열이름을 [행,열] 형식의 2차원 좌표로 입력하여 원소 위치 지정 할수 있다.
    - 인데스 이름 : DataFrame 객체.loc[행인덱스, 열이름]
    - 정수 위치 인덱스 : DataFrame 객체.iloc[행번호, 열이름]"""

sec_dpc.iloc[0] = 0  # iloc 사용할때는 첫번째 정수형 위치는 0 이다.
sec_dpc.head()

import matplotlib.pyplot as plt
sec_dpc = (sec['Close']/sec['Close'].shift(1)-1)*100
sec_dpc.iloc[0] = 0
plt.hist(sec_dpc, bins=18)  
'''히스토그램은 hist() 함수 사용, 데이터값들에 대한 구간별 빈도수를 막대 형태로 
나타냄, 구간수를 빈스라고 하는데 기본값은 10임''' 
plt.grid(True)
plt.show()

''' 주가 수익률이 정규분포와 비슷하다, 엄밀히 말하면 정규분포보다 중앙 부분이 더 뾰족하고 분포의 양쪽 꼬리는 더 두터운 것으로 알려져 있다.
    급첨분포와 팻 테일이라 부른다. 급첨분포는 주가 움직임이 대부분 매우 작은 범위안에서 발생, 팻테일은 그래프의 좌우 극단 부분에 
    해당하는 아주 큰 가격 변동이 정규분포보다 더 많이 발생 한다는 의미'''

sec_dpc.describe()
sec_dpc_cs = sec_dpc.cumsum() 
'''종목별로 전체적인 변동률을 비교해 보려면 일간 변동률 누적합 계산해야 함. 누적합은 cumsum() 함수 사용'''
sec_dpc_cs

sec = pdr.get_data_yahoo('005930.KS',start='2018-05-04')
sec_dpc = (sec['Close']- sec['Close'].shift(1))/sec['Close'].shift(1)*100
sec_dpc.iloc[0] = 0 # 일간 변동률의 첫번째 값인 NaN을 0으로 변경        
sec_dpc_cs = sec_dpc.cumsum()  # 일간 변동률의 누적합을 구한다.  
           
msft = pdr.get_data_yahoo('MSFT', start='2018-05-04')
msft_dpc = (msft['Close']/msft['Close'].shift(1)-1)*100
msft_dpc.iloc[0] = 0
msft_dpc_cs = msft_dpc.cumsum()           

plt.plot(sec.index, sec_dpc_cs, 'b', label='Samsung Electronics')
plt.plot(msft.index, msft_dpc_cs, 'r--', label='Microsoft')
plt.ylabel('Change %')
plt.grid(True)
plt.legend(loc='best')
plt.show()

# KOSPI 최대 손실 낙폭(MDD) 구하기
'''MDD는 특정기간에 발생한 최고점에서 최저점까지의 가장 큰 손실 (최저점-최고점)/최저점 
    퀀트투자에서는 수익률 높이는 것보다 MDD를 낮추는 것이 더낫다. 특정기간 동안 최대한 얼마의 손실이 날수 있는지 나타냄'''

kospi = pdr.get_data_yahoo('^KS11', '2004-01-04')  # KOSPI 지수의 심볼은 ^KS11
window = 252  # 산정기간에 해당하는 window는 개장일을 252로 어림잡아 설정
peak = kospi['Adj Close'].rolling(window, min_periods=1).max()  # 1년 기간 단위로 최고치 peak 구함
drawdown = kospi['Adj Close']/peak - 1.0  # drawdown 은 최고치 (peak) 대비 현재 KOSPI 종가가 얼마나 하락 했는지 구함
max_dd = drawdown.rolling(window, min_periods=1).min()  # 1년 기간 단위로 최저치 max_dd 구함
 
plt.figure(figsize=(9, 7))
plt.subplot(211)
kospi['Close'].plot(label='KOSPI', title='KOSPI MDD', grid=True, legend=True)
plt.subplot(212)
drawdown.plot(c='blue', label='KOSPI DD', grid=True, legend=True)
max_dd.plot(c='red', label='KOSPI MDD', grid=True, legend=True)
plt.show()

""" 통계 함수 적용
    1) 평균값 : 모든열의 평균값 DataFrame 객체.mean(),  특정열의 평균값 DataFrame 객체["열이름"].mean()
    2) 중간값 : 모든열의 중간값 DataFrame 객체.median(),  특정열의 중간값 DataFrame 객체["열이름"].median()
    3) 최대값 : 모든열의 최대값 DataFrame 객체.max(),  특정열의 최대값 DataFrame 객체["열이름"].max()
    4) 최소값 : 모든열의 최소값 DataFrame 객체.min(),  특정열의 최소값 DataFrame 객체["열이름"].min()
    5) 표쥰편차 : 모든열의 표준편차 DataFrame 객체.std(),  특정열의 표준편차 DataFrame 객체["열이름"].std()
    6) 상관계수 : 모든열의 상관계수 DataFrame 객체.corr(),  특정열의 상관계수 DataFrame 객체["열이름의 리스트"].corr()  """

max_dd.min()  # 정확한 MDD는 min() 함수 사용
max_dd[max_dd == -0.5453665130144085]  # 해당 손실한 기간 확인 방법

# OSPI 와 다우존스 지수 비교
dow = pdr.get_data_yahoo('^DJI', '2000-01-04')
kospi = pdr.get_data_yahoo('^KS11', '2000-01-04')

""" 판다스에서는 matplotlib()의 일부 기능 내장 되어 있어 plot() 메서드를 사용할수 있다.
    kind 옵션으로 그래프 종류 선택 가능 (line 선그래프, bar 수직 막대그래프, bath 수평막대 그래프, his 히스토그램
    box 박스플롯, scatter 산점도그래프 등) 예) 막대그래프 : DataFrame 객체.plot(kind='bar')
    옵션없으면 기본은 선그래프
    matplotlib 라이브러니는 파이썬 표준 시각화 도구로 2D 평면 그래프에 관한 다양한 포맷과 기능을 제공  """

import matplotlib.pyplot as plt
plt.figure(figsize=(9, 5))
plt.plot(dow.index, dow.Close, 'r--', label = 'Dow Jones Industrial')
plt.plot(kospi.index, kospi.Close, 'b', label = 'KOSPI')
plt.grid(True)
plt.legend(loc = 'best')
plt.show()

""" 지수 기준값이 달라서 어느 지수가 좋은 성과를 내는지 확인 불가. 
    일별 종가만으로는 상관관계 비교 어려움, 현재 종가를 특정시점의 종가로 나누어 변동률 확인 """

d = (dow.Close/dow.Close.loc['2000-01-04'])*100  
# 현재 다우존스 지수를 2000-01-04 지수로 나눈 뒤 100을 곱함. 2000-01-04 종가 대비 오늘의 변동률을 구할수 있다
k = (kospi.Close/kospi.Close.loc['2000-01-04'])*100

plt.figure(figsize=(9, 5))
plt.plot(d.index, d, 'r--', label = 'Dow Jones Industrial')
plt.plot(k.index, k, 'b', label = 'KOSPI')
plt.grid(True)
plt.legend(loc = 'best')
plt.show()

#산점도 분석 (X,Y의 상관관계 분석)
len(dow)
len(kospi)

df = pd.DataFrame({'DOW':dow['Close'], 'KOSPI':kospi['Close']})
df = df.fillna(method = 'bfill')
''' 누락데이터 (NaN)는 Excel의 경우 병합된 셀을 데이터프레임으로 변환할때 적절한 값을 찾지 못해서 발생
    fillna() 메소드의 mothod='ffill' 옵션을 이용하면 누락데이터가 들어 있는 행의 바로 앞에 위치한 행의 데이터 값으로 채운다.
    (NaN(값이 없다는 의미) Data를 뒤에 있는 값으로 덮어씀
    맨마지막에 NaN이 있으면 그럴때는 ffill() 방식으로 한번 더호출함으로써 마지막행의 이전 행에 있던 값으로 NaN을 덮어씀
    mothod='bfill' 옵션을 이용하면 누락데이터가 들어 있는 행의 바로 뒤에 위치한 행의 데이터 값으로 채운다.
    fillna() 메소드는 새로운 객체를 반환가히 때문에 원본 객체를 변경하려면 inplace=True 옵션 추가
    누락데이터 찾는 방법 
    1) isnull() 메서드 사용시 print(df.head().isnull()) 하면 첫5행의 원소들중 누락 데이터가 있는 부분은 True 를 반환
    2) notnull() 메서드 사용시 원소들중 누락 데이터가 있는 부분은 False 를 반환
    누락데이터가 많은면 해당 데이터는 제거한다. 결과값을 왜곡한다.
    중복 데이터 확인에는 duplicated() 메서드 이용  -> DataFrame.duplicated()'''

# 상관관계 분석할 데이터의 숫자가 같아야 한다. 위와 같이 조치를 안해도 산점도가 그려짐 (아래 코드)

dow = pdr.get_data_yahoo('^DJI', '2000-01-04')
kospi = pdr.get_data_yahoo('^KS11', '2000-01-04')

df = pd.DataFrame({'DOW': dow['Close'], 'KOSPI': kospi['Close']})
df = df.fillna(method='bfill')
df = df.fillna(method='ffill')

plt.figure(figsize=(7, 7))
plt.scatter(df['DOW'], df['KOSPI'], marker='.')
plt.xlabel('Dow Jones Industrial Average')
plt.ylabel('KOSPI')
plt.show()

''' 점의 분포가 Y=X인 직선 형태에 가까울수록 직접적인 관계가 있다. 아래 그래프를 볼때 어느정도 영향을 미치긴 하지만 그리 강하지 않다.
    정확한 분석이 어려우므로 선형 회귀 분석으로 더 정확히 분석히 분석해야함'''

'''사이파이(scipy)는 파이썬 기반 수학,과학,엔지니어링용 핵심 패키지 모음. 넘파이 기반 함수, 수학적 알고리즘 모음으로 넘파이, 
    맷플롯립, 심파이, 팬더스 등을 포함. 사이파이 패키지 중 서브패키지는 stats는 다양한 통계 함수를제공'''

from scipy import stats
regr = stats.linregress(df['DOW'], df['KOSPI'])
'''상관계수는 상관관계 정도를 나타내는 수치임. 상관계수 r은 항상 -1 <= r <= 1 데이터프레임은 상관계수를 구하는 corr() 함수를 제공'''
df.corr()  # 상관계수는 0.749364임

# 시리즈도 corr()함수 제공, 인수로 상관계수를 구할 다른 시리즈 객체 넣어줌

df['DOW'].corr(df['KOSPI'])  # df.DOW.corr(df.KOSPI)와 같다
yf.pdr_override()

dow = pdr.get_data_yahoo('^DJI', '2000-01-04')  # 자료 다운로드
kospi = pdr.get_data_yahoo('^KS11', '2000-01-04')

df = pd.DataFrame({'X':dow['Close'], 'Y':kospi['Close']}) # 데이터프레임 생성
df = df.fillna(method='bfill') # NaN 값 제거 (뒤에값으로 덮어씀)
df = df.fillna(method='ffill') # NaN 값 제거 (앞에값으로 덮어씀)

regr = stats.linregress(df.X, df.Y) # 선형 회귀모델 객체 생성
regr_line = f'Y = {regr.slope:2f}  X + {regr.intercept:2f}' # 범례에 회귀식 표현

plt.figure(figsize=(7, 7))  # figure() 함수로 그림틀의 가로 사이즈를 설정
plt.plot(df.X, df.Y, '.')  # 산점도를 작은원'.'으로 표현
plt.plot(df.X, regr.slope * df.X + regr.intercept, 'r')  # 회귀선을 붉은색으로 그림
plt.legend(['DOW x KOSPI', regr_line])
plt.title(f'DOW x KOSPI (R = {regr.rvalue:2f})')  # 챠트 제목 추가 .title() 메서드 사용
plt.xlabel('Dow Jones Industrial Average')  # X축 이름 xlabel() 메서드 사용
plt.ylabel('KOSPI')  # y축 이름 xlabel() 메서드 사용
plt.show()

""" matplotlib 는 한글폰트 지원 안함. 파이썬 프로그램 앞부분에 한글 폰트를 지정하는 다음 코드 추가
    matplotlib 한글폰트 오류 문제 해결
    from matplotlib import font_manager, rc
    font_path = "./malgun.ttf"  # 폰트 파일 위치
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name) 
    위 코드 삽입후 자료실에서 한글 폰트 파일을 다운로드 받아서 파이썬 파일과 같은 폴더에 저장 또는 
    윈도우 설치 폴더에서 사용할 한글폰트를 찾아서 파일 경로를 font_path 에 할당하는 방법도 가능

    노벨경제학상 수상한 해리 마코위츠 박사가 체계화한 현대 포트폴리오 이론은 투자에 대한 수익과 위험은 평균과 분산으로 나타낼수 있으며, 
    상관관계가 낮은 자산을 대상으로 분산 투자하면 위험을 감소시킬수 있다는 이론이다.
    상관계수에 따른 리스크 완화 효과
    1. +1.0  리스크 완화 효과가 없음
    2. +0.5  중간 정도의 리스크 완화 효과가 있음
    3.  0    상당한 리스크 완화 효과가 있음
    4. -0.5  대부분의 리스크를 제거함
    5. -1.0  모든 리스크 제거함 """
