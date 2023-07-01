from django.urls import path
from .post_views import *
from .comment_views import *

app_name = 'community'

urlpatterns = [
    # 게시글 R ----------
    path('', community_list, name='community_list'),
    path('<int:post_id>/', community_detail, name='community_detail'),
    # 게시글 C, U, D
    path('create/', create_post, name='create_post'), #글작성
    path('delete/<int:post_id>/', delete_post, name='delete_post'), #삭제
    path('modify/<int:post_id>/', modify_post, name='modify_post'), #수정
     # 댓글 CRUD ------------
    path('comment/create/post/<int:post_id>/', comment_create, name='comment_create'),
    path('comment/modify/post/<int:comment_id>/', comment_modify, name='comment_modify'),
    path('comment/delete/post/<int:comment_id>/', comment_delete, name='comment_delete'),
]