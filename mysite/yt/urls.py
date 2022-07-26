from django.urls import path, include
from . import views
from .setup import setup_urls
from .tag import tag_urls
from .board import board_urls

app_name = 'yt'

urlpatterns = [
    path('', views.index, name='index'),
    path('setup', views.setup, name='setup'),
    path('setup/', include(setup_urls.setup_patterns), name='setup'),
    path('search', views.search, name='search'),
    path('tag/', include(tag_urls.tag_patterns), name='tag'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('board/', include(board_urls.board_patterns), name='board'),
    path('practice/',views.practice,name='practice'),
    path('loginpractice/',views.loginpractice,name='loginpractice'),
]
