from django.urls import path
from .views import *

app_name = 'community'

urlpatterns = [
    path('', community_list, name='community_list'),
    path('<int:post_id>/', community_detail, name='community_detail'),
    path('create/', create_post, name='create_post'), #글작성
    path('delete/<int:post_id>/', delete_post, name='delete_post'), #삭제
    path('modify/<int:post_id>/', modify_post, name='modify_post'), #수정
]