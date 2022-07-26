from django.urls import path
from . import views

setup_patterns = [
    path('Tag', views.setup_Tag, name='setup_Tag'),
    path('Channel', views.setup_Channel, name='setup_Channel'),
    path('update/channel', views.UPDATE, name='update_Channel'),
    path('update/keywordTag', views.make_keywordTag, name='setup_keywordTag'),
]