from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from .models import *


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'status', 'avatar']
        widget = {
            'avatar': forms.ImageField,
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш никнейм"})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль"})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль ещё раз"})
        self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите описание вашего профиля"})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш адрес эл. почты"})
        self.fields['avatar'].widget.attrs.update({'default': 'photos/user.png', 'placeholder': "ваш аватар"})

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title', ]

    def __init__(self, *args, **kwargs):
        super(CreateCategoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': "Введите название категории"})


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})
    new_password1 = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})
    new_password2 = forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'status', 'avatar']
        widget = {
            'avatar': forms.ImageField,
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите ваш никнейм"})
        self.fields['status'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите статус вашего профиля"})
        self.fields['avatar'].widget.attrs.update({})

        for fieldname in ['username']:
            self.fields[fieldname].help_text = None


class ProfileForm(forms.Form):
    status = forms.TextInput(attrs={'class': 'form-control'})
    avatar = forms.ImageField(label='avatar', required=False)


class CustomChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'status']


class UserLoginForm(AuthenticationForm):
    # username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'})),
    email = forms.EmailField,
    password1 = forms.TextInput,
    password2 = forms.TextInput,

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'введите ваш никнейм'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': "введите пароль"})


class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['title', 'text', 'level', 'category', 'image']

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Заголовок:'})
        self.fields['text'].widget.attrs.update({'class': 'form-control', 'placeholder': "Текст:", 'rows': 6})
        self.fields['level'].widget.attrs.update({'class': 'form-control col-md-1', 'placeholder': "Уровень доступа"})
        self.fields['category'].widget.attrs.update({'class': 'form-control col-md-3', 'placeholder': "Категория"})

