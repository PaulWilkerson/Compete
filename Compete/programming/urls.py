from django.urls import path
from . import views

urlpatterns = [
    path('challenges/', views.challenge_list, name='programming_challenge_list'),
    path('challenges/<int:challenge_id>/', views.challenge_detail, name='programming_challenge_detail'),
    path('execute/', views.execute_code, name='execute_code'),
    path('new/', views.new_challenge, name='programming_new_challenge'),
]
