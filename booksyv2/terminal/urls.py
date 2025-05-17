from django.urls import path
from . import views
from .Functionalities import Login,calendar,Appointment_booking


urlpatterns = [
    path('home/', views.home,name='home'),
    path('', Login.login_user, name='login'),
    path('logout/', Login.logout_user, name='logout'),
    path('register/', Login.register_user, name='register'),
    path('booking/', Appointment_booking.booking, name='booking'),
    path('employee/', calendar.CalendarView.as_view(), name='calendar'),
    path('add_appointment/', Appointment_booking.add_appointment,name = 'add_appointment')
    ]