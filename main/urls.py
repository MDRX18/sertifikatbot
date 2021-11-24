from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('getpost/', views.getpost),
    path('setwebhook/', views.setwebhook),
]



