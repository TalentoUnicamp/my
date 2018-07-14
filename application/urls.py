from django.urls import path
from .views import ApplicationView

app_name = 'application'
urlpatterns = [
    path('', ApplicationView.as_view(), name='form')
]
