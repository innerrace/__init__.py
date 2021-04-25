"""investar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views (URL 설정을 위한 3가지 방식)
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from balance import views as balance_views
from index import views as index_views
from hello import views  # from 애플리케이션명 import views 형식으로 hello 애플리케이션의 views 를 임포트
from django.urls import path, re_path  # django.urls 로부터 re_path() 함수를 추가적으로 임포트

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^(?P<name>[A-Z][a-z]*)$', views.sayHello),
    path('index/', index_views.main_view),
    path('balance/', balance_views.main_view),
]

# urlpatterns 리스트의 마지막에 hello 애플리케이션의 URL 에 대한 뷰처리를 추가
# path() 함수와 달리 re_Path() 함수를 사용하면 정규표현식을 사용해 URL 패턴 처리 가능
# path('index/', index_views.main_view) 는 index 애플리케이션 설치후 URL 이 'index/'이면 index 애플리케이션
# 뷰의 main_view() 함수로 매핑하라는 의미
