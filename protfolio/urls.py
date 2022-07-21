from django.contrib import admin
from django.urls import path
from protfolio import views

urlpatterns = [
    path('', views.index, name="home"),
    path('about/', views.about, name="about"),
    path('resume/', views.resume, name="resume"),
    path('contact/', views.contact, name="contact"),
    path('control_panel/', views.control_panel, name="control_panel"),
    path('message_list/', views.messages_list, name="message_list"),
    path('delete_message/<int:mid>/', views.delete_messages, name="delete_message"),
    path('logout/', views.logout_view, name="logout"),
    path('education/', views.education, name="education"),
    path('work-experience/', views.workexperience, name="work-experience"),
]
