from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url('login', views.login1, name='login1'),
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    
]