from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('auth-success', views.auth_success, name='auth_success'),
    path('polls', views.polls, name='polls'),
    path('details/<int:poll_id>', views.details, name='details'),
]