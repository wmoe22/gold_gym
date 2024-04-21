from django.contrib import admin

# Register your models here.
from .models import User,Exercises

admin.site.register(User)
admin.site.register(Exercises)