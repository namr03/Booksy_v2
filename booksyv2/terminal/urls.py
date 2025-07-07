from django.urls import path
from . import views
from .Functionalities import Login,calendar,Appointment_booking
from .Functionalities import editting_account

urlpatterns = [
    path('home/', views.home,name='home'),
    path('', Login.login_user, name='login'),
    path('logout/', Login.logout_user, name='logout'),
    path('register/', Login.register_user, name='register'),
    path('booking/', Appointment_booking.booking, name='booking'),
    path('employee/', calendar.CalendarView.as_view(), name='calendar'),
    path('add_appointment/', Appointment_booking.add_appointment,name = 'add_appointment'),
    path('appointments/', Appointment_booking.appointments, name='appointments'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),
    path('cancel_appointment/<int:appointment_id>/', Appointment_booking.cancel_appointment, name='cancel_appointment'),
    path('edit_profile/', editting_account.edit_profile, name='edit_profile'),
    ]