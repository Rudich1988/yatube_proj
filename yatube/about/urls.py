from django.urls import path

from .views import AboutAuthorView, TechTemplateView

app_name = 'about'


urlpatterns = [
    path('about_author/', AboutAuthorView.as_view(), name='about_author'),
    path('tech/', TechTemplateView.as_view(), name='tech')
]
