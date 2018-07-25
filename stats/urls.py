from django.urls import path, include
from . import views, api

apipatterns = [
    path('hacker_stats/', api.HackerStats.as_view(), name='hacker_stats')
]

app_name = 'stats'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('', views.StatsView.as_view(), name='index'),
]
