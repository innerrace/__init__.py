from meme_mothod.DualMomentum import *

start_date = '2020-01-01'
end_date = '2020-06-30'
stock_count = 300

""" 6개월 상대 모멘텀 """
dm = DualMomentum()
rm = dm.get_rltv_momentum(start_date, end_date, stock_count)

""" 6개월 절대 모멘텀 """
am = dm.get_abs_momentum(rm, start_date, end_date)

""" 3개월 한국형 듀얼모멘텀 (한국시장에서는 3개월 전략이 훨씬 수익률이 좋음)
    한국 자산만으로 운영하는 전략에는 3개월 듀얼모멘텀을 적용하고, 한국 자산과 해외 혼합하는 경우에는 12개월 듀얼 모멘텀을 
    적용하는 한국형 전략도 고려해 볼만하다.
    또한 90일 미국 국채를 직접 매수하는 대신 'iShares 20 + Year Treasury Bond ETF(TLT)' 같은 ETF에 투자할 경우,
    미국 국체 수익률을 추종하면서 환 헤지까지 할수 있는 한국 투자자만의 장점이 있다. 
    백테스트 해볼때 3개월 및 종목수를 줄일때 수익률이 증가하는 경향이 높다"""

start_date = '2020-03-01'
end_date = '2020-06-30'
stock_count = 10
rm = dm.get_rltv_momentum(start_date, end_date, stock_count)