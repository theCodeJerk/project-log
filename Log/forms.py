from django import forms
from Log.models import LogEntry
from martor.fields import MartorFormField


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = '__all__'
        widgets = {
            'content': MartorFormField,
            'user': forms.HiddenInput,
        }