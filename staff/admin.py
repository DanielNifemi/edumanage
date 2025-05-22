from django.contrib import admin
from .models import Department, Role, StaffProfile, LeaveRequest, PerformanceEvaluation

admin.site.register(Department)
admin.site.register(Role)
admin.site.register(StaffProfile)
admin.site.register(LeaveRequest)
admin.site.register(PerformanceEvaluation)
