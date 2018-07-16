from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = []

if settings.DEBUG:
    urlpatterns += [
        path('test/', TemplateView.as_view(template_name='model_sockets/test.html'))
    ]
