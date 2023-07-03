#from datetime import datetime as dt
#from typing import Any, Dict

from common.views import TitleMixin
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetConfirmView,
                                       PasswordResetView)
#from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView

from .forms import (EmailForm, PasswordSetForm, UserLoginForm,
                    UserPasswordChangeForm, UserRegistrationForm)
from .models import User


class UserRegistrationview(TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    title = 'Регистрация'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()        
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain_name = settings.DOMAIN_NAME
        token = default_token_generator.make_token(user)
        link = reverse_lazy('users:email_confirm', kwargs={'uidb64': uid, 'token': token})
        link_ver = f'{domain_name}{link}'        
        send_mail(
            subject='Подтвердите свой электронный адрес',
            message=f'Перейдите по ссылке: {link_ver}, чтобы подтвердить регистрацию',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        title = 'Письмо активации отправлено'
        return render(self.request, 'users/email_confirmation_sent.html', context={'title': title})
    

class EmailConfirm(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            title = 'Поздравляем, Вы активированы!'
            return render(request, 'users/email_confirmed.html', context={'title': title})            
        else:
            title = 'Ваша электронная почта не активирована'
            return render(request, 'users/email_confirmation.html', context={'title': title})


class UserLoginView(TitleMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Авторизация'

    def get_success_url(self):
        return reverse_lazy('posts:index')


def logoutview(request):
    logout(request)
    return redirect('users:login')


class PasswordChangeFormView(PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')

    def get_context_data(self, **kwargs):
        context = super(PasswordChangeFormView, self).get_context_data(**kwargs)
        context['us'] = self.request.user
        context['title'] = f'Изменение пароля для пользователя: {self.request.user.username}'
        return context


class PasswordChangeDone(TemplateView):
    template_name = 'users/password_change_done.html'


class PasswordResetFormView(TitleMixin ,PasswordResetView):
    form_class = EmailForm
    template_name = 'users/password_reset_form.html'
    success_url = reverse_lazy('users:password_reset_done')
    from_email = settings.EMAIL_HOST_USER
    title = 'Восстановление пароля'


class PasswordResetDoneView(TemplateView):    
    template_name = 'users/password_reset_done.html'


class PasswordResetConfView(TitleMixin ,PasswordResetConfirmView):
    form_class = PasswordSetForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

    def get_context_data(self, **kwargs):
        context = super(PasswordResetConfView, self).get_context_data(**kwargs)
        context['uidb64'] = self.kwargs.get('uidb64')
        context['token'] = self.kwargs.get('token')
        context['user'] = self.user
        context['title'] = f'Восстановление пароля для пользователя: {self.user}'
        return context


class PasswordResetComplete(TemplateView):
    template_name = 'users/password_reset_complete.html'
