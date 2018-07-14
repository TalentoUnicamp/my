from django.urls import path, include
from . import views, api

apipattens = [
    path('unlink_provider/', api.UnlinkProvider.as_view(), name='unlink_provider'),
]

app_name = 'social'

urlpatterns = [
    path('api/', include((apipattens, 'api')), name='api'),

    path('login/<str:provider>/', views.SocialLogin.as_view(), name='login'),
    path('login_response/<str:provider>/', views.SocialLoginResponse.as_view(), name='login_response')
]
