from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('', views.dashboard, name='dashboard'),
]
