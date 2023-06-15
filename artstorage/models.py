from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.views import View


def user_directory_path(instance, filename):
    return 'accounts/{0}/{1}'.format(instance.slug, 'avatar')
class User(AbstractUser):
    slug = models.SlugField(verbose_name='Слаг', unique=True)
    descriptions = models.TextField(max_length=300, verbose_name='Описание',blank=True)
    email = models.EmailField(verbose_name='Почта',blank=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True, verbose_name="Фото")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        # Slugify (Cyrillic)
        alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                    'и': 'i',
                    'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
                    'ю': 'yu',
                    'я': 'ya'}

        self.slug = slugify(''.join(alphabet.get(w, w) for w in self.username.lower()))
        super(User, self).save(*args, **kwargs)

    def get_short_name(self):
        return f"{self.first_name} {self.last_name}"
    def get_projects(self):
        return Project.objects.all().filter(user=self)

    def get_views(self):
        count = 0
        for proj in self.get_projects():
            count+=proj.count_watches
        return count

    def count_projects(self):
        return self.get_projects().count()

    def get_followers(self):
        return Follow.objects.all().filter(follow_from_id=self.id).values_list('follow_to', flat=True)

    def count_followers(self):
        return self.get_followers().count()

    def get_followings(self):
        return Follow.objects.all().filter(follow_to_id=self.id).values_list('follow_from', flat=True)

    def count_followings(self):
        return Follow.objects.all().filter(follow_to_id=self.id).count()

    def get_absolute_url(self):
        return reverse('profile', kwargs={'slug': self.slug})

    def get_first_projects(self):
        return self.get_projects().order_by('count_watches')[:3]


class Follow(models.Model):
    follow_from = models.ForeignKey('User', related_name='follower', on_delete=models.CASCADE, verbose_name='Кто подписался')
    follow_to = models.ForeignKey('User', related_name='following',on_delete=models.CASCADE, verbose_name='На кого подписался')
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['id']


def project_directory_path(instance, filename):
    return 'projects/{0}/{1}'.format( instance.name, filename)
class Project(models.Model):
    slug = models.SlugField(verbose_name='Слаг', unique=False)
    name = models.CharField(max_length=50, db_index=True, verbose_name="Название")
    photo = models.ImageField(upload_to=user_directory_path, blank=True, verbose_name="Фото")
    user = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='Юзер')
    count_watches = models.IntegerField(default=0, verbose_name='Количество просмотров')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")


    def save(self, *args, **kwargs):
        # Slugify (Cyrillic)
        alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
                    'и': 'i',
                    'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
                    'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e',
                    'ю': 'yu',
                    'я': 'ya'}
        self.slug = slugify(''.join(alphabet.get(w, w) for w in self.name.lower()))
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project', kwargs={'project_slug': self.slug, 'user_slug': self.user.slug})


    def get_count_likes(self):
        return Like.objects.filter(project_liked=self).count()


    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['id']

class ViewModel(models.Model):
    project_watch = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')
    user_watch = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Проект')

class Like(models.Model):
    user_liked = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='юзер')
    project_liked = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name='Проект')