from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime

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