from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from Log.models import LogEntry, Project
from martor.fields import MartorFormField


class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['username'].widget.attrs['readonly'] = True

    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.username
        else:
            return self.cleaned_data['username']

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', )


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
