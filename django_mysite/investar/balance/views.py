from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_data(symbol):
    url = 'http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        cur_price = soup.find('strong', id='_nowVal')
        # id 가 _nowVal인 <strong> 태그 찾아 cur_price 변수에 현재가 태그가 저장
        cur_rate = soup.find('strong', id='_rate')
        # id 가 _rate인 <strong> 태그 찾아 cur_rate 변수에 등락률을 태그가 저장
        stock = soup.find('title')  # title 태그를 찾아 stock 변수에 저장
        stock_name = stock.text.split(':')[0].strip()
        # title 태그에서 콜론(':') 문자를 기준으로 문자열을 분리하여 종목명을 구한뒤 문자열 좌우의 공백문자를 제거한다.
        return cur_price.text, cur_rate.text.strip(), stock_name


def main_view(request):
    querydict = request.GET.copy()
    mylist = querydict.lists()
    # GET 방식으로 넘어온 QueryDict 형태의 URL 을 리스트 형태로 변환
    rows = []
    total = 0

    for x in mylist:
        cur_price, cur_rate, stock_name = get_data(x[0])
        # mylist 의 종목코드로 get_data 함수를 호출하여 현재가, 등락률, 종목명을 구함
        price = cur_price.replace(',', '')
        stock_count = format(int(x[1][0]), ',')
        # mylist 의 종목수를 int 형으로 변환한뒤, 천자리마다 쉼표(',')를 포함하는 문자열로 변환
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',')
        rows.append([stock_name, x[0], cur_price, stock_count, cur_rate, stock_sum])
        # 종목명, 종목코드, 현재가, 주식수, 등락률, 평가금액을 리스트로 생성하여 rows 리스트에 추가
        total = total + int(price) * int(x[1][0])  # 평가금액을 주식수로 곱한뒤 total 변수에 더함

    total_amount = format(total, ',')
    values = {'rows': rows, 'total': total_amount}  # balance.html 파일에 전달할 값들을 values 딕셔너리에 저장
    return render(request, 'balance.html', values)
    # balance.html 파일을 표시하도록 render() 함수를 호출하여 인수값에 해당하는 values 딕셔너리를 넘겨준다
