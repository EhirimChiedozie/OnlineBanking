"""bank_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from customers import views as customer_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bankapp.urls') ),
    path('open_account/', customer_views.open_account, name='open_account'),
    path('login/', auth_views.LoginView.as_view(template_name='customers/login.html'), name='customers_login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='customers/logout.html'), name='customers_logout'),
    path('profile', customer_views.profile, name='customers_profile'),
    path('confirm_logout/', customer_views.confirm_logout, name='confirm_logout'),
    path('make_transfer_request/', customer_views.make_transfer_request, name='make_transfer_request'),
    path('confirm_transfer_details/', customer_views.confirm_transfer_details, name='confirm_transfer_details'),
    path('execute_transfer/', customer_views.execute_transfer, name='execute_transfer'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='customers/password_reset.html'), name='password_reset'),
    path('password_reset_confirm/<uidb64><token>/', auth_views.PasswordResetConfirmView.as_view(template_name='customers/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='customers/password_reset_complete.html'), name='password_res3et_complete'),
    path('statement/', customer_views.CustomerStatementView.as_view(), name='statement'),
]
