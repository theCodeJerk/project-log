from django.shortcuts import render
from django.views.generic import TemplateView
from Log.models import LogEntry
from Log.forms import NewEntryForm
from martor.models import MartorFormField
from django.contrib.auth.models import User

def index_view(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            form.save()
    else:
        form = NewEntryForm(initial={'user': request.user})
    context = {'form': form,
               'title': 'Project Log',
               'logentries': LogEntry.objects.filter(user=request.user).all()
               }
    return render(request, 'pages/index.html', context)

