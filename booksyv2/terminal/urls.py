from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home,name='home'),
    path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('booking/', views.booking, name='booking'),
    path('employee/', views.CalendarView.as_view(), name='calendar'),
    path('add_appointment/', views.add_appointment,name = 'add_appointment')
    ]