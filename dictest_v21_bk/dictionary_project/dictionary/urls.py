from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('random/', views.random_word, name='random_word'),
    path('search/suggestions', views.search_suggestions, name='search_suggestions'),
    path('word/<int:pk>/', views.word_detail, name='word_detail'),
    path('users/', include('users.urls')),
]