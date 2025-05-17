from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import *
from datetime import datetime
import uuid

@login_required
def booking(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user)
    
    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        
        # Validate if service and time are in allowed choices
        valid_services = [choice[0] for choice in SERVICE_CHOICE]
        valid_times = [choice[0] for choice in TIME_CHOICES]
        
        if service not in valid_services:
            messages.error(request, "Invalid service selected")
            return redirect('booking')
            
        if time not in valid_times:
            messages.error(request, "Invalid time selected")
            return redirect('booking')
            
        # Check if appointment time is available
        if Appointment.objects.filter(day=day, time=time).exists():
            messages.error(request, "This time slot is already booked")
            return redirect('booking')
            
        # Create new appointment
        try:
            appointment = Appointment.objects.create(
                user=user,
                service=service,
                day=datetime.strptime(day, '%Y-%m-%d').date(),
                time=time,
                time_ordered=datetime.now()
            )
            messages.success(request, f"Successfully booked {service} for {day} at {time}")
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Booking failed: {str(e)}")
            return redirect('booking')
    
    context = {
        'services': SERVICE_CHOICE,
        'times': TIME_CHOICES,
        'appointments': appointments,
        'today': datetime.now().date()
    }
    
    return render(request, 'terminal/terminal.html', context)

@login_required
def add_appointment(request):
    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Validate if service and time are in allowed choices
        valid_services = [choice[0] for choice in SERVICE_CHOICE]
        valid_times = [choice[0] for choice in TIME_CHOICES]
        
        if service not in valid_services:
            messages.error(request, "Invalid service selected")
            return redirect('calendar')
            
        if time not in valid_times:
            messages.error(request, "Invalid time selected")
            return redirect('calendar')
            
        # Check if appointment time is available
        if Appointment.objects.filter(day=day, time=time).exists():
            messages.error(request, "This time slot is already booked")
            return redirect('calendar')
        #Check if user exists if not, it creates new user
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            temp_password = str(uuid.uuid4())[:8]
            user = MyUser.objects.creating_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone,
                password=temp_password,
            )

        # Create new appointment
        try:
            appointment = Appointment.objects.create(
                user=user,
                service=service,
                day=datetime.strptime(day, '%Y-%m-%d').date(),
                time=time,
                time_ordered=datetime.now()
            )
            messages.success(request, f"Successfully booked {service} for {day} at {time}")
        except Exception as e:
            messages.error(request, f"Booking failed: {str(e)}")
            
    return redirect('calendar')
