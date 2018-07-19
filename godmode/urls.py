from django.urls import path, include
from . import views, api

apipattens = [
    path('toggle_is_admin/', api.ToggleIsAdmin.as_view(), name='toggle_is_admin'),
    path('delete_user/<str:unique_id>/', api.DeleteUser.as_view(), name='delete_user'),
    path('batch_create_users/', api.BatchCreateUsers.as_view(), name='batch_create_users'),
]

app_name = 'godmode'
urlpatterns = [
    path('api/', include((apipattens, 'api')), name='api'),
    path('', views.AdminView.as_view(), name='index')
]
