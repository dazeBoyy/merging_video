from django.urls import path,include
from . import views

from django.conf.urls import url



urlpatterns = [

path('register', views.register, name="register"),
path('login_user', views.login_user, name="login_user"),
path('logout_user', views.logout_user, name="logout_user"),

path('home', views.UploadFile, name='home'),
path('view', views.ViewFile, name='ViewFile'),

path('<str:name>', views.view_video, name='view_video'),



url(r'^clear/$', views.clear_database, name='clear_database'),
]