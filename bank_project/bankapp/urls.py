from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bankapp_home'),
    path('about/', views.about, name='bankapp_about'),
]