from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, View, ListView

from artstorage.models import User, Project, ViewModel, Follow, Like
def like(request):
    from django.shortcuts import redirect

    project = request.GET.get('project_id')
    project = Project.objects.get(id=project)
    if not request.user.is_authenticated:
        return redirect('login')
    if Like.objects.filter(user_liked=request.user, project_liked=project).count() == 0:
        a = Like(user_liked=request.user, project_liked=project)
        a.save()
    return redirect('project', user_slug=project.user.slug, project_slug=project.slug)


def index(request):
    return render(request, 'artstorage/index.html')


def authors(request):
    return render(request, 'artstorage/authors.html')
class AuthorsView(ListView):
    paginate_by = 3
    model = User
    template_name = 'artstorage/authors.html'
    context_object_name = 'authors'

    def get_queryset(self):
        return User.objects.order_by('-time_create')

def pictures(request):
    return render(request, 'artstorage/pictures.html')


def projects(request):
    return render(request, 'artstorage/pictures.html')
class ProjectsView(ListView):
    model = Project
    paginate_by = 9
    template_name = 'artstorage/pictures.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.all().order_by('-time_create')
def registration(request):
    from artstorage.forms import CustomUserCreationForm
    if request.method == "GET":
        form = CustomUserCreationForm()
        return render(request, 'artstorage/registration.html', {'form':form})
    else:
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            pass1 = request.POST['password1']

            new_user = authenticate(username=username, password=pass1)
            login(request, new_user)
            return redirect('home')
        else:
            return render(request, 'artstorage/registration.html', {'form': form})

class LoginUser(LoginView):
    template_name = 'artstorage/authorization.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Авторизация"
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def authorization(request):
    return render(request, 'artstorage/authorization.html')

def profile(request):
    return render(request, 'artstorage/update-profile.html')
class Profile(DetailView):
    model = User
    template_name = 'artstorage/profile.html'
    context_object_name = 'user'

    def get(self, request, *args, **kwargs):
        from artstorage.forms import CreateProject
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        user_profile = get_object_or_404(User,slug=slug)
        is_your_profile = False
        if request.user.is_authenticated:
            if user_profile.id == request.user.id:
                is_your_profile = True
                # Пользователь открывает свой профиль

          # Пользователь открывает профиль другого пользователя
        form = CreateProject()
        return render(request, 'artstorage/profile.html', {'user': user_profile,
                                                           'is_your_profile': is_your_profile,
                                                           'projects':user_profile.get_projects(),
                                                           'title': slug,
                                                           'form': form})

class ProfileUpdateView(UpdateView):
    model = User
    enctype = "multipart/form-data"
    fields = ['descriptions', 'photo']
    template_name = 'artstorage/update-profile.html'
    context_object_name = 'user'

    '''def get_success_url(self):
        return reverse_lazy('profile',kwargs = {'slug': self.request.user.slug})'''
    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        user_profile = get_object_or_404(User, slug=slug)
        if request.user.is_authenticated:
            if user_profile.id == request.user.id:
                self.object = self.get_object()
                return super().get(request, *args, **kwargs)
        raise PermissionDenied()
    def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(User, slug=self.kwargs.get(self.slug_url_kwarg, None))

        return  super().post(request, args, kwargs)

    def get_context_data(self, *, object_list = None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['title'] = "Редактирование профиля"
        from artstorage.forms import CreateProject
        context['formProj'] = CreateProject()
        return context

class ProjectsUser(ListView):
    paginate_by = 3
    model = Project
    template_name = 'artstorage/author-profile.html'
    context_object_name = 'projects'
    def get_queryset(self):
        user = get_object_or_404(User, slug = self.request.path_info.split('/')[2])
        return user.get_projects()
    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, slug = self.request.path_info.split('/')[2])
        context['user'] = user
        if self.request.user.is_authenticated:
            context['is_not_your_profile'] = self.request.user.slug != user.slug
        else:
            context['is_not_your_profile'] = True
        return context



def picture_description(request):
    return render(request, 'artstorage/picture-description.html')


def personal_profile_projects(request):
    return render(request, 'artstorage/../templates/personal-profile-projects.html')


def personal_profile_pictures(request):
    return render(request, 'artstorage/../templates/personal-profile-pictures.html')

class ProjectView(DetailView):
    model = Project

    template_name = 'artstorage/picture-description.html'
    def get_object(self, queryset=None):
        slug_user = self.kwargs['user_slug']
        slug_project = self.kwargs['project_slug']
        user = User.objects.get(slug=slug_user)
        return user.get_projects().get(slug=slug_project)
    def get_context_data(self, **kwargs):
        slug_user = self.kwargs['user_slug']
        slug_project = self.kwargs['project_slug']

        user = User.objects.get(slug=slug_user)
        project = user.get_projects().get(slug=slug_project)

        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['project'] = project
        if self.request.user.is_authenticated:
            context['is_not_your_profile'] = self.request.user.slug != user.slug
            if ViewModel.objects.filter(project_watch=project).filter(user_watch=self.request.user).count() == 0:
                project.count_watches += 1
                project.save()
                a = ViewModel(project_watch=project, user_watch=self.request.user)
                a.save()
        else:
            context['is_not_your_profile'] = True



        return context


def logout_user(request):
    logout(request)
    return redirect('home')
def AddProject(request):
    print(request.POST)
    print(request.FILES)
    name=request.POST.get('name')
    image=request.FILES.get('image')
    a = Project(name=name, photo=image, user=request.user)
    a.save()
    return redirect('profile', slug = request.user.slug)

class SubscribeView(View):
    def post(self, request):
        from django.shortcuts import redirect

        profile_id = request.POST.get('user_id')
        redirect_url = request.POST.get('redirect_url')
        profile = User.objects.get(id=profile_id)
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user == profile:
            return redirect(redirect_url)

        a = Follow(follow_from=request.user, follow_to=profile)
        a.save()

        return redirect(redirect_url)

class UnsubscribeView(View):
    def post(self, request):
        profile_id = request.POST.get('user_id')
        redirect_url = request.POST.get('redirect_url')
        profile = User.objects.get(id=profile_id)
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user == profile:
            return redirect(redirect_url)

        Follow.objects.filter(follow_from=request.user, follow_to=profile).delete()

        return redirect(redirect_url)