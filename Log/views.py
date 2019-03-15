from django.shortcuts import render, redirect
from Log.models import LogEntry, Project
from Log.forms import *


def index_view(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()

    context = {'form': NewEntryForm(initial={'user': request.user}),
               'title': 'Project Log',
               'logentries': LogEntry.objects.filter(user=request.user).all(),
               }
    return render(request, 'pages/index.html', context)


def projects_view(request):
    if request.method == 'POST':
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


def delete_entry_view(request, entry_id):
    entry = LogEntry.objects.get(id=entry_id)
    if request.method == 'POST':
        form = DeleteEntryForm(request.POST)
        if form.is_valid():
            LogEntry.delete(entry)
            return redirect('index')
    else:
        form = DeleteEntryForm(instance=entry)

    context = {'form': form,
               'title': 'Projects',
               'projects': Project.objects.filter(user=request.user).all(),
               'entry': entry,
               'disable_actions': True,
               }
    return render(request, 'pages/delete-entry.html', context)


def edit_entry_view(request, entry_id):
    entry = LogEntry.objects.get(id=entry_id)
    if request.method == 'POST':
        form = EditEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.instance.save()
            return redirect('index')
    else:
        form = EditEntryForm(instance=entry)

    context = {'form': form,
               'title': 'Projects',
               'projects': Project.objects.filter(user=request.user).all(),
               'entry': entry,
               'disable_actions': True,
               }
    return render(request, 'pages/edit-entry.html', context)


def edit_project_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = EditProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.instance.save()
            return redirect('projects')
    else:
        form = EditProjectForm(instance=project)

    context = {'form': form,
               'title': 'Edit Project',
               'project': project,
               }
    return render(request, 'pages/edit-project.html', context)


def delete_project_view(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = DeleteProjectForm(request.POST)
        if form.is_valid():
            Project.delete(project)
            return redirect('projects')
    else:
        form = DeleteProjectForm(instance=project)

    context = {'form': form,
               'title': 'Delete Project',
               'project': project,
               'disable_actions': True,
               }
    return render(request, 'pages/delete-project.html', context)
