from django.urls import include, path
from . import api

apipatterns = [
    path('settings/', api.SettingsView.as_view(), name='get_update')
]

app_name = 'settings'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api')
]
