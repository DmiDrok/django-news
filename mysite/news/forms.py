from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import New, Category
from captcha.fields import CaptchaField


class AddNewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'

    class Meta:
        model = New
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Введите заголовок'}),
            'slug': forms.TextInput(attrs={'placeholder': 'Введите URL'})
        }

# Форма для регистрации
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Ваш логин'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Ваша почта'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Пароль ещё раз'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get('password1')
    #     password2 = self.cleaned_data.get('password2')

    #     if password1 != password2:
    #         return forms.ValidationError('Пароли не совпадают!')

    #     return password2

# Форма авторизации
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Ваш логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Ваш пароль'}))

    class Meta:
        model = User
        fields = ['username', 'password']


# Форма обратной связи
class ContactForm(forms.Form):
    username = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    email = forms.EmailField(label='Ваш Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    content = forms.CharField(label='Ваше сообщение', widget=forms.Textarea(attrs={'rows': 5, 'cols': 30}))
    captcha = CaptchaField()