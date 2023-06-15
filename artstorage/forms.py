from django.contrib.auth.forms import UserCreationForm
from django import forms
from artstorage.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email',  'password1', 'password2')
        help_texts = {
            'username': None,
            'first_name': None,
            'last_name': None,
            'email': None,
            'password1': None,
            'password2': None,
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password2'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['username'].help_text = None
        self.fields['email'].help_text = None
        self.fields['first_name'].help_text = None
        self.fields['last_name'].help_text = None
        list = ['Логин', 'Имя', 'Фамилия', 'Почта', 'Пароль', 'Повторите пароль']
        i=0
        for visible in self.visible_fields():
            print(visible)
            visible.field.widget.attrs['class'] = 'input enter-input'
            visible.field.widget.attrs['placeholder'] = list[i]
            i+=1

class CreateProject(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'data__name', 'type':"text", 'id':"project-name", 'placeholder': 'Название'}))
    image = forms.ImageField(max_length=100, widget=forms.FileInput(attrs={'class': 'visually-hidden', 'type':"file", 'id':"choose-personal-project"}))

