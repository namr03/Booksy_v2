from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@login_required
def home(request):
    services = Service.objects.all()
    user = request.user
    appointments = Appointment.objects.filter(user=user).order_by('day','time')
    
    # Generate available dates for next 7 days
    today = datetime.now()
    available_dates = []
    
    for i in range(7):
        current_date = today + timedelta(days=i)
        available_dates.append({
            'day': current_date.day,
            'weekday': current_date.strftime('%a'),
            'value': current_date.strftime('%Y-%m-%d'),
            'today': i == 0
        })
    
    context = {
        'services': services,
        'times': TIME_CHOICES,
        'today': today.date(),
        'appointments': appointments,
        'available_dates': available_dates,
    }
    return render(request, 'terminal/terminal.html', context)

@require_GET
def get_available_times(request):
    service_id = request.GET.get('service')
    date = request.GET.get('date')
    
    # Get service duration and calculate available slots
    service = Service.objects.get(id=service_id)
    
    # Get all existing appointments for this date
    booked_times = Appointment.objects.filter(
        service=service,
        day=date
    ).values_list('time', flat=True)
    
    # Generate all possible time slots
    all_slots = []
    start_time = datetime.strptime('09:00', '%H:%M')
    end_time = datetime.strptime('17:00', '%H:%M')
    slot_duration = timedelta(minutes=service.duration)
    
    current_slot = start_time
    while current_slot + slot_duration <= end_time:
        time_str = current_slot.strftime('%H:%M')
        if time_str not in booked_times:
            all_slots.append({
                'value': time_str,
                'display': time_str
            })
        current_slot += slot_duration

    return JsonResponse({'times': all_slots})