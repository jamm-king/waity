from django.urls import path, include
from . import views
from django.conf.urls import url


game_patterns = [
    path('', views.game, name='game'),
    path('leagueoflegend', views.leagueoflegend, name='leagueoflegend'),
    path('battleground', views.battleground, name='battleground'),
    path('overwatch', views.overwatch, name='overwatch'),
    path('starcraft', views.starcraft, name='starcraft'),
    path('maplestory', views.maplestory, name='maplestory'),
    path('minecraft', views.minecraft, name='minecraft'),
    path('fifa', views.fifa, name='fifa'),
]
music_patterns = [
    path('', views.music, name='music'),
    path('sing', views.sing, name='sing'),
    path('piano', views.piano, name='piano'),
    path('mv', views.mv, name='mv'),
    path('classic', views.classic, name='classic'),
    path('audition', views.audition, name='audition'),
    path('hiphop', views.hiphop, name='hiphop'),
    path('trott', views.trott, name='trott'),
    path('popsong', views.popsong, name='popsong'),
    path('kpop', views.kpop, name='kpop'),
]
sports_patterns = [
    path('', views.sports, name='sports'),
    path('soccer', views.soccer, name='soccer'),
    path('basketball', views.basketball, name='basketball'),
    path('baseball', views.baseball, name='baseball'),
    path('golf', views.golf, name='golf'),
    path('tennis', views.tennis, name='tennis'),
]
entertain_patterns = [
    path('', views.entertain, name='entertain'),
    path('idol', views.idol, name='idol'),
    path('play', views.play, name='play'),
]
tag_patterns = [
    path('game/', include(game_patterns), name='game'),
    path('music/', include(music_patterns), name='music'),
    path('sports/', include(sports_patterns), name='sports'),
    path('entertain/', include(entertain_patterns), name='entertain'),
    path('eat/', views.eat, name='eat'),
    path('knowledge/', views.knowledge, name='knowledge'),
    path('review/', views.review, name='review'),
    path('documentary/', views.documentary, name='documentary'),
    path('vlog/', views.vlog, name='vlog'),
    path('all/', views.all, name='all'),
]
