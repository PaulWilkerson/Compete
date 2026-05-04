from django.urls import path
from . import views

urlpatterns = [
    path('challenges/', views.challenge_list, name='cli_challenge_list'),
    path('challenges/<int:challenge_id>/', views.challenge_detail, name='cli_challenge_detail'),
    path('execute/<int:challenge_id>/', views.execute_code, name='execute_code'),
    path('new/', views.new_challenge, name='cli_new_challenge'),
]
