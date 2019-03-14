from django.shortcuts import render, redirect
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


def add_project_view(request):
    form = NewProjectForm(request.POST, initial={'user': request.user})
    if form.is_valid():
        form.save()
        return redirect('projects')
    else:
        form = NewProjectForm(initial={'user': request.user})
        context = {'form': form,
                   'title': 'Projects',
                   'projects': Project.objects.filter(user=request.user).all(),
                   }
        return render(request, 'pages/add-project.html', context)
