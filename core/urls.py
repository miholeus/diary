# coding: utf-8

from django.urls import path
from . import views

__author__ = 'miholeus'

"""Core URL Configuration.
"""

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('registration/', views.RegistrationView.as_view(), name='registration'),
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/add', views.NewUserView.as_view(), name='users.add'),
    path('users/edit/(<int:id>)/', views.EditUserView.as_view(), name='users.edit'),
    path('users/delete/(<int:id>)/', views.RemoveUserView.as_view(), name='users.delete'),
    path('users/profile/(<int:id>)/', views.UserProfileView.as_view(), name='users.profile'),
    path('trainings/', views.TrainingsListView.as_view(), name='trainings'),
    path('trainings/add', views.TrainingsNewView.as_view(), name='trainings.add'),
]

