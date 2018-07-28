from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import api
from . import views

apipattens = [
    path('check_token/', api.CheckToken.as_view(), name='check_token'),
    path('change_email/', api.ChangeEmail.as_view(), name='change_email'),
    path('change_token/', api.ChangeToken.as_view(), name='change_token'),
    path('reset_token_email/', api.ResetTokenEmail.as_view(), name='reset_token_email'),
    path('list_profiles/', api.ListProfiles.as_view(), name='list_profiles'),
    path('list_hacker_profiles/', api.ListHackerProfiles.as_view(), name='list_hacker_profiles'),
    path('sui_list_profiles/', api.SUIListProfiles.as_view(), name='sui_list_profiles'),
]

app_name = 'profile'
urlpatterns = [
    path('api/', include((apipattens, 'api')), name='api'),
    path('logout/', LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
    path('token_login/<str:token>/', views.TokenLoginView.as_view(), name='token_login'),
    path('verify_email/<str:code>/', views.VerifyEmailView.as_view(), name='verify_email'),
]
