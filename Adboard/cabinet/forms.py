from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from cabinet.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', "autofocus": True}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', "autocomplete": "current-password"}))
    email = forms.EmailField(label='Введите почту', widget=forms.EmailInput(attrs={'class': 'form-input'}))


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', min_length=3, max_length=30, widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Введите почту', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Такой email уже существует")
        return email


class UpdateUserForm(forms.ModelForm):
    """
    Изменение данных пользователя.
    Проверка введенных значений в форме не отслеживается, проверяю через сериалайзер
    """

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'photo', 'date_birth']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'photo': forms.FileInput(attrs={'accept': 'jpg'}),
            'date_birth': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя пользователя',
            'last_name': 'Фамилия пользователя',
            'email': 'Почта',
            'photo': 'Аватарка',
            'date_birth': 'Дата рождения',
        }

