import requests
'''requests 패키지에서 제공하는 get(), post() 함수를 사용위해 import'''
from PIL import Image
'''get 요청한 이미지 객체를 처리하기 위해 import'''
import hashlib
'''해시값 확인'''
import matplotlib.pyplot as plt
'''파이썬의 데이터 시각화 라이브러리로 각종 그래프를 그리거나 이미지 처리에 사용'''
import matplotlib.image as mpimg

# 2.8.1 리퀘스트로 인터넷에서 이미지 파일 가져오기
url = 'https://www.mirandakerr.com/wp-content/uploads/2020/05/Miranda-Kerr-Connect-Sitting-By-Desk.jpg'
r = requests.get(url, stream=True).raw

# 2.8.2 필로우로 이미지 보여주기
img = Image.open(r)
print("img : ", img.get_format_mimetype)
img.show()
''' requests로 받은 응답객체를 이미지로 열때 show() 함수 사용'''
img.save('src.png')
'''저장할때 save() 함수 사용'''
''' 이미지 정보를 얻기 위해서는 get_format_mimetype 속성 출력
print(img.et_format_mimetype) 사용해서 정보 알수 있음'''

# 2.8.3 'with ~ as 파일 객체:'로 이미지 파일 복사
BUF_SIZE = 1024
with open('src.png', 'rb') as sf, open('dst.png', 'wb') as df:
    while True:
        data = sf.read(BUF_SIZE) 
        '''read(), write() 함수에 인수를 주지 않으면 힌꺼번에 모든 내용을 읽거나쓴다
        파일 크기가 수백메가나 기가 단위로 크면 문제 발생 일정한 길이로 나누어 
        읽고 쓰는 것이 좋다'''
        if not data:
            break
        df.write(data)

# 2.8.4 SHA-256으로 파일 복사 검증하기
sha_src = hashlib.sha256()
sha_dst = hashlib.sha256()
'''해시는 긴데이터 값을 입력받아서 고정 길이의 고유한 값으로 변환하는것이 핵심
해시는 입력값이 같으면 생성되는 해시값도 같아서 파일의 변경 여부를 파악하거나
두 파일의 내용이 동일한지 비교 하는데 주로 사용
SHA-256은 256비트, 즉 64바이트의 해시값'''

with open('src.png', 'rb') as sf, open('dst.png', 'rb') as df:
    sha_src.update(sf.read())  
    sha_dst.update(df.read())

print("src.png's hash : {}".format(sha_src.hexdigest()))
print("dsc.png's hash : {}".format(sha_dst.hexdigest()))
'''원본이미지 파일과 사본 이미지 파일의 해시값을 16진수로 출력
   64비트가 아니고 16바트를 출력한것은 hexdigest() 메서드를 사용했기 때문'''

# 2.8.5 맷플롯립으로 이미지 가공하기
'''맷플롯립은 기본적을 PNG 이비미 포맷만 지원 '''
plt.suptitle('Image Processing', fontsize=18)
plt.subplot(1, 2, 1) # 인수를 1,1,1처럼 쉼표로 구분 1행 2열의 영역에서 첫 번째 영역으로 지정
'''subplot() 함수로 두 이미지를 나란히 표시'''
plt.title('Original Image')
plt.imshow(mpimg.imread('src.png')) # 원본 파일을 읽어서 이미지로 표시

plt.subplot(122) # 1행 2열의 영역에서 두 번째 영역으로 지정 
plt.title('Pseudocolor Image')
dst_img = mpimg.imread('dst.png')
pseudo_img = dst_img [:, :, 0]  # 의사 색상 적용
plt.imshow(pseudo_img) 
plt.show()