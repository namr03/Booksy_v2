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
    
    # Generate available dates for next 15 days
    today = datetime.now()
    available_dates = []
    
    for i in range(15):
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
    
    # Different handling for manicure/pedicure vs other services
    if service.name in ['Manicure', 'Pedicure']:
        # Get all appointments for manicure and pedicure
        manicure_pedicure_services = Service.objects.filter(name__in=['Manicure', 'Pedicure'])
        booked_appointments = Appointment.objects.filter(
            service__in=manicure_pedicure_services,
            day=date
        )
    else:
        # For other services, only check appointments for the same service
        booked_appointments = Appointment.objects.filter(
            service=service,
            day=date
        )

    # Calculate blocked time slots
    booked_slots = set()
    for appointment in booked_appointments:
        appointment_start = datetime.strptime(appointment.time, '%H:%M')
        appointment_end = appointment_start + timedelta(minutes=appointment.service.duration)
        
        # Block all slots that overlap with this appointment
        current = appointment_start
        while current < appointment_end:
            booked_slots.add(current.strftime('%H:%M'))
            current += timedelta(minutes=30)

    # Generate all possible time slots
    all_slots = []
    start_time = datetime.strptime('10:00', '%H:%M')
    end_time = datetime.strptime('20:00', '%H:%M')
    slot_duration = timedelta(minutes=service.duration)
    
    current_slot = start_time
    while current_slot + slot_duration <= end_time:
        time_str = current_slot.strftime('%H:%M')
        
        # Check if slot is available
        is_available = True
        check_time = current_slot
        while check_time < current_slot + slot_duration:
            if check_time.strftime('%H:%M') in booked_slots:
                is_available = False
                break
            check_time += timedelta(minutes=30)
        
        if is_available:
            all_slots.append({
                'value': time_str,
                'display': time_str
            })
        current_slot += slot_duration

    return JsonResponse({'times': all_slots})