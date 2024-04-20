from django.contrib import admin

# Register your models here.
from .models import User,Exercises,Streak

admin.site.register(User)
admin.site.register(Exercises)
admin.site.register(Streak)