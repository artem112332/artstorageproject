"""
URL configuration for artstoragedjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.urls import path
from artstorage.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),

    path('authors', AuthorsView.as_view(), name='authors'),
    path('pictures', ProjectsView.as_view(), name='pictures'),
    path('projects', ProjectsView.as_view(), name='projects'),
    path('registration', registration, name='registration'),
    path('authorization', LoginUser.as_view(), name='authorization'),
    path('logout', logout_user, name='logout'),
    path('profile/<slug:slug>', ProjectsUser.as_view(), name='profile'),
    path('profile/<slug:slug>/edit', ProfileUpdateView.as_view(), name='editProfile'),
    path('add_project', AddProject, name='addProject'),
    path('profile', profile, name='profile1'),
    path('project/<slug:user_slug>/project/<slug:project_slug>', ProjectView.as_view(), name='project'),
    path('personal-profile-projects', personal_profile_projects, name='personal-profile-projects'),
    path('personal-profile-pictures', personal_profile_pictures, name='personal-profile-pictures'),
    path('subscribe', SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe', UnsubscribeView.as_view(), name='unsubscribe'),
    path('like', like, name='like')

]




urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
