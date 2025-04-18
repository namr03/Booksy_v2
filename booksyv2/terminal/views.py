from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime

#Those are registration, login and logout functions
def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'terminal.backends.EmailBackend'
            login(request,user)
            messages.success(request,"Registration succesful")
            return redirect('home')
        else:
            messages.error(request,"Registration Failed")
    else:
        form = UserRegistrationForm()
    return render(request, 'terminal/register.html',{'form': form})

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request,user)
            messages.success(request,'Login successfull')
            return redirect('home')
        else:
            messages.error(request,"Invalid email or password")
    return render(request,'terminal/login.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out succesfully')
    return redirect('login')

@login_required
def home(request):
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day','time')
    context = {
        'services': SERVICE_CHOICE,
        'times': TIME_CHOICES,
        'today': datetime.now().date(),
        'appointments': appointments
    }
    return render(request, 'terminal/terminal.html', context)

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