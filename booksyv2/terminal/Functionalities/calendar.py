from ..models import Appointment, Service, TIME_CHOICES
from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
from django.views import generic
from django.utils.safestring import mark_safe
import calendar

class Calendar(HTMLCalendar):
    def __init__(self, year = None, month = None, user = None):
        self.year= year
        self.month= month
        self.user = user
        super(Calendar,self).__init__()
    
    def formatday(self, day, appointments):
        d = ''
        if day != 0:
            current_day = date(self.year, self.month, day)
            is_past = current_day < datetime.now().date()
            appointments_per_day = appointments.filter(day__day=day)
            for appointment in appointments_per_day:
                is_worker = self.user in appointment.service.workers.all()
                appointment_class = "appointment"
                if is_worker:
                    appointment_class += " worker-appointment"
                d += f'''
                        <div class="{appointment_class}">
                            <span class="time">{appointment.time}</span>
                            <span class="service">{appointment.service}</span>
                            <span class="client">{appointment.user.first_name} {appointment.user.last_name}</span>
                        </div>
                    '''
            cell_class = 'past-day' if is_past else 'day-cell'
            return f'''
                <td class = "{cell_class}">
                    <div class="date-container">
                       <span class="date">{day}</span>
                       <button class="add-appointment-btn" onclick="showAppointmentForm('{self.year}-{self.month:02d}-{day:02d}')" style="display: { 'none' if is_past else 'block' }">
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
        cal = Calendar(d.year, d.month, user=self.request.user)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['services'] = Service.objects.all()
        context['times'] = TIME_CHOICES
        return context