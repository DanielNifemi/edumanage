from django.contrib import admin
from .models import InfractionType, DisciplinaryAction, DisciplinaryRecord, BehaviorNote

admin.site.register(InfractionType)
admin.site.register(DisciplinaryAction)
admin.site.register(DisciplinaryRecord)
admin.site.register(BehaviorNote)