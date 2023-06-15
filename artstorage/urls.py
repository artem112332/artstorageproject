'''from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
urlpatterns = [
    path('', index, name='home'),
    path('authors', authors, name='authors'),
    path('pictures', pictures, name='pictures'),
    path('projects', projects, name='projects'),
    path('registration', registration, name='registration'),
    path('authorization', LoginUser.as_view(), name='authorization'),
    path('profile/<slug:slug>', Profile.as_view(), name='profile'),
    path('profile/<slug:slug>/edit', ProfileUpdateView.as_view(), name='editProfile'),
    path('profile', profile, name='profile'),
    path('picture-description', picture_description, name='picture-description'),
    path('personal-profile-projects', personal_profile_projects, name='personal-profile-projects'),
    path('personal-profile-pictures', personal_profile_pictures, name='personal-profile-pictures'),

]
urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)'''