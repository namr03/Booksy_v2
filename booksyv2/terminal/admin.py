from django.contrib import admin
from .models import MyUser,Service

admin.site.register(MyUser)
admin.site.register(Service)