from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.tweet_list, name='tweet_list'),
    path('create/', views.tweet_create, name='tweet_create'),
    path('<int:tweet_id>/edit/', views.tweet_edit, name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete, name='tweet_delete'),
    path('register/', views.register, name='register'),
    path('search/', views.seacrh_tweets, name='search_tweets'),
    path('<int:tweet_id>/detail/', views.tweet_detail, name='tweet_detail'),
    path('<int:tweet_id>/comment/', views.add_comment, name='add_comment'),
    path('profile/<str:username>', views.profile_view, name='profile_detail'),
    path('Edit_profile/', views.profile_edit, name='profile_edit'),
]
