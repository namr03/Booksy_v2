from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import *
from datetime import datetime, timedelta
import uuid

@login_required
def booking(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user)
    services = Service.objects.all()  # Get all available services
    today = datetime.now()
    
    # Generate available dates
    available_dates = []
    for i in range(15):
        current_date = today + timedelta(days=i)
        available_dates.append({
            'day': current_date.day,
            'weekday': current_date.strftime('%a'),
            'value': current_date.strftime('%Y-%m-%d'),
            'today': i == 0
        })
    
    if request.method == 'POST':
        service_id = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        try:
            service_obj = Service.objects.get(id=service_id)
            
            # Create appointment
            appointment = Appointment.objects.create(
                user=user,
                service=service_obj,
                day=datetime.strptime(day, '%Y-%m-%d').date(),
                time=time,
                time_ordered=datetime.now()
            )
            messages.success(request, f"Successfully booked {service_obj.name} for {day} at {time}")
            return redirect('appointments')
        except Exception as e:
            messages.error(request, f"Booking failed: {str(e)}")
            return redirect('booking')
    
    context = {
        'services': services,  # Changed from service_obj to services
        'appointments': appointments,
        'available_dates': available_dates,
        'today': today.date()
    }
    
    return render(request, 'terminal/terminal.html', context)

@login_required
def add_appointment(request):
    if request.method == 'POST':
        service_id = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            service_obj = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            messages.error(request, "Invalid service selected")
            return redirect('booking')
            
        valid_times = [choice[0] for choice in TIME_CHOICES]
            
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
                service=service_obj,
                day=datetime.strptime(day, '%Y-%m-%d').date(),
                time=time,
                time_ordered=datetime.now()
            )
            messages.success(request, f"Successfully booked {service_obj.name} for {day} at {time}")
        except Exception as e:
            messages.error(request, f"Booking failed: {str(e)}")
            
    return redirect('calendar')

@login_required
def appointments(request):
    today = datetime.now().date()
    
    # Get future appointments
    future_appointments = Appointment.objects.filter(
        user=request.user,
        day__gte=today
    ).order_by('day', 'time')
    
    # Get past appointments
    past_appointments = Appointment.objects.filter(
        user=request.user,
        day__lt=today
    ).order_by('-day', '-time')  # Note the minus for reverse chronological order
    
    context = {
        'future_appointments': future_appointments,
        'past_appointments': past_appointments
    }
    return render(request, 'terminal/my_appointments.html', context)

@login_required
def cancel_appointment(request, appointment_id):
    appointment = Appointment.objects.filter(id=appointment_id, user=request.user).first()
    if appointment:
        appointment.delete()
        messages.success(request, "Appointment cancelled successfully.")
    else:
        messages.error(request, "Appointment not found or not authorized.")
    return redirect('appointments')