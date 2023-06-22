from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),   #회원가입
    path('login/', views.login_view, name='login'), #로그인
    path('logout/', views.logout_view, name='logout'), #로그인
]
