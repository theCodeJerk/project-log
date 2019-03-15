from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from martor.models import MartorField


class Project(models.Model):
    name = models.CharField(unique=True, max_length=64, blank=False, null=False)
    description = MartorField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta():
        db_table = 'pl_project'


class LogEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logentry_user")
    creation_dt = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE)
    content = MartorField(null=False, blank=False)

    def __str__(self):
        return self.content

    class Meta():
        db_table = 'pl_logentry'
        ordering = ['-creation_dt',]

    def edit_url(self):
        return reverse('edit-entry', args=[self.pk])

    def delete_url(self):
        return reverse('delete-entry', args=[self.pk] )
