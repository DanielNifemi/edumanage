from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body', 'attachment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['recipient'].queryset = self.fields['recipient'].queryset.exclude(id=user.id)


class ForwardMessageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body', 'attachment']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ForwardMessageForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['recipient'].queryset = self.fields['recipient'].queryset.exclude(id=user.id)