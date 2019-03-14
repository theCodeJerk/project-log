from django.db import models
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
    content = MartorField()

    def __str__(self):
        return self.content

    class Meta():
        db_table = 'pl_logentry'
