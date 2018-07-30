from django.urls import path, include
from . import views, api

apipatterns = [
    path('hacker_stats/', api.HackerStats.as_view(), name='hacker_stats'),
    path('hacker_signup_list/', api.HackerSignupList.as_view(), name='hacker_signup_list'),
    path('hacker_application_list/', api.HackerApplicationList.as_view(), name='hacker_application_list'),
]

app_name = 'stats'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('', views.StatsView.as_view(), name='index')
]
