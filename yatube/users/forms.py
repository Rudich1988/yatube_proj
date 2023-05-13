from django import forms
from django.conf import settings
from django.contrib.auth.forms import (AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm,
                                       UserCreationForm)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя'
    }))    
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя пользователя'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите адрес электронной почты'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
    
    
class EmailForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите адрес эл.почты'
    }))    
    
    class Meta:
        model = User
        fields = ('email',)

    def send_email(self, *args, **kwargs):
        try:
            user = User.objects.get(email=self.cleaned_data['email'])
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            link = reverse_lazy('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            link_ver = f'Перейдите по ссылке {settings.DOMAIN_NAME}{link}'
        except:
            user = None
            token = 'not_active_token'
            uidb64 = 'user_none'
            link = reverse_lazy('users:password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            link_ver = f'Для изменения пароля перейдите по ссылке {settings.DOMAIN_NAME}{link}'
        send_mail(
            subject='Изменение пароля',
            message=link_ver,
            from_email=kwargs.get('from_email'),
            recipient_list=[self.cleaned_data['email']],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):        
        apts = {
        'from_email': kwargs.get('from_email'),
        }
        self.send_email(**apts)

        
class PasswordSetForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите новый пароль'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model=User
        fields = ('new_password1', 'new_password2')
    


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите старый пароль'
    }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите новый пароль'
    }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите новый пароль'
    }))

    class Meta:       
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
