import json
import os
import uuid
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from martor.utils import LazyEncoder
from django.conf import settings
from Log.models import LogEntry, Project
from Log.forms import *
from django.utils.translation import ugettext_lazy as _


def index_view(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()

    context = {'form': NewEntryForm(initial={'user': request.user}),
               'title': 'Project Log',
               'logentries': LogEntry.objects.filter(user=request.user).all(),
               'user': request.user,
               'hide_sidepanel': True,
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
               'user': request.user,
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
                   'user': request.user,
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
               'user': request.user,
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
               'user': request.user,
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
               'user': request.user,
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
               'user': request.user,
               }
    return render(request, 'pages/delete-project.html', context)


def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))