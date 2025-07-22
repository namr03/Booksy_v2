from django.contrib import admin
from .models import MyUser,Appointment,Service

admin.site.register(MyUser)
admin.site.register(Appointment)
admin.site.register(Service)