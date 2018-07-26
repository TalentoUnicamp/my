from django.urls import path, include
from . import views, api

apipatterns = [
    path('view_application/<str:unique_id>/', api.ViewApplication.as_view(), name='view_application'),
    path('form_options/<str:option>/', api.FormOptionsAPI.as_view(), name='form_options'),
]

app_name = 'application'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('', views.ApplicationView.as_view(), name='form')
]
