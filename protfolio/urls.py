from django.contrib import admin
from django.urls import path
from protfolio import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/',views.about, name="about"),
    path('resume/',views.resume, name="resume"),
    path('contact/', views.contact, name="contact")
]