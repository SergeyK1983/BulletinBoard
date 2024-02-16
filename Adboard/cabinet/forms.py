from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

from cabinet.models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
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
    # username = forms.CharField(label='Логин', disabled=True, widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            # 'photo': forms.ImageField(),
        }
        labels = {
            'first_name': 'Имя пользователя',
            'last_name': 'Фамилия пользователя',
            # 'photo': 'Фотография'
        }

    # if email is None:  # проверка
    #     raise ValidationError("Должен быть хотя бы один символ")
    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get("email")
    #     if email is None:  # проверка
    #         raise ValidationError({
    #             "email": "Должен быть хотя бы один символ"
    #         })

