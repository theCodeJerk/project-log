from django import forms
from Log.models import LogEntry, Project
from martor.fields import MartorFormField


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = '__all__'
        widgets = {
            'content': MartorFormField,
            'user': forms.HiddenInput,
        }


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'content': MartorFormField,
            'user': forms.HiddenInput,
        }


class DeleteEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = 'id',
        widgets = {
            'id': forms.HiddenInput,
        }


class EditEntryForm(forms.ModelForm):
    class Meta:
        model = LogEntry
        fields = '__all__'
        widgets = {
            'content': MartorFormField,
            'user': forms.HiddenInput,
        }


class EditProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'name': forms.TextInput,
            'description': MartorFormField,
            'user': forms.HiddenInput,
        }


class DeleteProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = 'id',
        widgets = {
            'id': forms.HiddenInput,
        }
