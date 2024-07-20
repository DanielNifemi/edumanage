from django import forms
from .models import DisciplinaryRecord, BehaviorNote


class DisciplinaryRecordForm(forms.ModelForm):
    class Meta:
        model = DisciplinaryRecord
        fields = ['infraction_type', 'date', 'description', 'action_taken', 'action_date', 'resolved',
                  'resolution_notes']


class BehaviorNoteForm(forms.ModelForm):
    class Meta:
        model = BehaviorNote
        fields = ['date', 'note']
