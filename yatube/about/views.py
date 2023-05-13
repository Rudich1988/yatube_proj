from django.shortcuts import render
from django.views.generic.base import TemplateView

from common.views import TitleMixin


class AboutAuthorView(TitleMixin ,TemplateView):

    template_name = 'about/about_author.html'
    title = 'Об авторе'


class TechTemplateView(TitleMixin, TemplateView):

    template_name = 'about/tech.html'
    title = 'Технологии'

