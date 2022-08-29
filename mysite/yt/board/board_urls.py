from django.urls import path, include
from . import views

board_patterns = [
    path('', views.Board_list, name='boardList'),
    path('write/', views.Board_write, name='boardWrite'),
    path('detail/<int:pk>/', views.Board_detail, name='boardDetail'),
    path('new_comment/<int:post_id>', views.new_comment, name='new_comment'),
    path('delete/comment/<int:comment_id>', views.CommentDelete, name='commentDelete'),
    path('modify/comment/<int:comment_id>', views.CommentModify, name='commentModify'),
    path('modify/<int:board_id>', views.BoardModify, name='boardModify'),
    path('myBoard/', views.myBoard, name='myBoard'),
    path('myBoard/detail/<int:pk>/', views.Board_detail),
    path('myBoardDelete/', views.myBoardDelete, name='myBoardDelete'),
    path('<str:category_name>/', views.Board_category, name='boardCategory'),
]
