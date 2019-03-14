from django.shortcuts import render
from Log.models import LogEntry, Project
from Log.forms import NewEntryForm, NewProjectForm


def index_view(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
    else:
        form = NewEntryForm(initial={'user': request.user})
    context = {'form': form,
               'title': 'Project Log',
               'logentries': LogEntry.objects.filter(user=request.user).all(),
               }
    return render(request, 'pages/index.html', context)


def projects_view(request):
    if request.method == "POST":
        form = NewProjectForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
    else:
        form = NewProjectForm(initial={'user': request.user})
    context = {'form': form,
               'title': 'Projects',
               'projects': Project.objects.filter(user=request.user).all(),
               }
    return render(request, 'pages/projects.html', context)
