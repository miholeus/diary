# coding: utf-8

from django.conf.urls import url
from . import views

__author__ = 'miholeus'

"""Core URL Configuration.
"""

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^registration/$', views.RegistrationView.as_view(), name='registration'),
]

