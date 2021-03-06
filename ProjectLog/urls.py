"""ProjectLog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.urls import include
from Log.views import *
from martor.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(
            template_name='registration/login.html',
        ),
        name='login',
        ),
    path('accounts/profile/', login_required(profile_view), name='profile'),
    path('accounts/logout/', login_required(LogoutView.as_view()), name='logout'),
    path('projects/', login_required(projects_view), name='projects'),
    path('projects/add/', login_required(add_project_view), name='add-project'),
    path('entry/delete/<entry_id>', login_required(delete_entry_view), name='delete-entry'),
    path('entry/edit/<entry_id>', login_required(edit_entry_view), name='edit-entry'),
    path('project/edit/<project_id>', login_required(edit_project_view), name='edit-project'),
    path('project/delete/<project_id>', login_required(delete_project_view), name='delete-project'),
    path('api/uploader/', login_required(markdown_uploader), name='markdown_uploader_page'),
    path('martor/', include('martor.urls')),
    path('', login_required(index_view), name='index'),
]


# make it possible to serve files in debug mode locally
if settings.DEBUG is True:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
