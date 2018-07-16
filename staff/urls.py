from django.urls import path, include
from . import views, api

apipatterns = [
    path('toggle_is_staff/', api.ToggleIsStaff.as_view(), name='toggle_is_staff'),
    path('create_blank_hacker/', api.CreateBlankHacker.as_view(), name='create_blank_hacker'),
]

app_name = 'staff'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('', views.StaffView.as_view(), name='index'),
]
