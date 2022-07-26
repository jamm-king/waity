from django.contrib import admin
from django.urls import include, path
from yt.views import setup

from yt import views

urlpatterns = [
    path('', include('yt.urls', namespace='yt')),
    path('admin/', admin.site.urls),
    path('admin/setup', views.setup)
]
