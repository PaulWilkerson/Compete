from django.urls import path
from . import views

urlpatterns = [
    path('challenges/', views.challenge_list, name='cyber_challenge_list'),
    path('challenges/<int:challenge_id>/', views.challenge_detail, name='cyber_challenge_detail'),
    path('new/', views.new_challenge, name='cyber_new_challenge'),
]