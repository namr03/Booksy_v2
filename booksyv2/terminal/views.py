from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import *
from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
from django.utils.safestring import mark_safe
from django.views import generic
import calendar

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
            if user.is_superuser:
                login(request,user)
                messages.success(request,'Login successfull as employee')
                return redirect('calendar')
            else:    
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

@login_required
def add_appointment(request):
    if request.method == 'POST':
        service = request.POST.get('service')
        day = request.POST.get('day')
        time = request.POST.get('time')
        
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
            
        # Create new appointment
        try:
            appointment = Appointment.objects.create(
                user=request.user,
                service=service,
                day=datetime.strptime(day, '%Y-%m-%d').date(),
                time=time,
                time_ordered=datetime.now()
            )
            messages.success(request, f"Successfully booked {service} for {day} at {time}")
        except Exception as e:
            messages.error(request, f"Booking failed: {str(e)}")
            
    return redirect('calendar')
#Created class for Calendar with functions that format day, week and month
class Calendar(HTMLCalendar):
    def __init__(self, year = None, month = None):
        self.year= year
        self.month= month
        super(Calendar,self).__init__()
    
    def formatday(self, day, appointments):
        d = ''
        if day != 0:
            appointments_per_day = appointments.filter(day__day=day)
            for appointment in appointments_per_day:
                d += f'''
                        <div class="appointment">
                            <span class="time">{appointment.time}</span>
                            <span class="service">{appointment.service}</span>
                            <span class="client">{appointment.user.first_name} {appointment.user.last_name}</span>
                        </div>
                    '''
            return f'''
                <td class = "day-cell">
                    <div class="date-container">
                       <span class="date">{day}</span>
                       <button class="add-appointment-btn" onclick="showAppointmentForm('{self.year}-{self.month:02d}-{day:02d}')">
                           +
                       </button>
                    </div>
                    <div class="appointments-container">
                        {d}
                    </div>
                </td>
            '''
        return '<td></td>'
    
    def formatweek(self, theweek, appointments):
        week = ''
        for d,weekday in theweek:
            week += self.formatday(d,appointments)
        return f'<tr>{week}</tr>'
    
    def formatmonth(self,withyear = True):
        appointments = Appointment.objects.filter(
            day__year = self.year,
            day__month = self.month
        ).order_by('time')

        cal = f'<table class="calendar">\n'
        cal += f'{self.formatmonthname(self.year,self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year,self.month):
            cal += f'{self.formatweek(week, appointments)}\n'

        return cal
    #It returns actual day or first day of the month
def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year,month,day=1)
    return datetime.today()
    #it checks previous month converting month as string to be use in URL
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month
    #Same as prev but next instead of previous
def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
#Class for viewing calendar with appointments 
class CalendarView(generic.ListView):
    model = Appointment
    template_name = 'terminal/employee_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context