from django.contrib import admin
from .models import TimeSlot, DayOfWeek, Schedule, Event

admin.site.register(TimeSlot)
admin.site.register(DayOfWeek)
admin.site.register(Schedule)
admin.site.register(Event)