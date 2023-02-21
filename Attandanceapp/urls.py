from django.contrib import admin
from django.urls import path,include
from Attandanceapp import views

urlpatterns = [
    path('login', views.login,name="LoginPage"),
    path('Attandance',views.submit)
]