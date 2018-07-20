from django.urls import path, include
from django.contrib import admin
from django.conf import settings
import debug_toolbar
from .views import LoginView
admin.autodiscover()
# from app import views

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('profile/', include('user_profile.urls')),
    path('social/', include('social.urls')),
    path('settings/', include('settings.urls')),
    path('application/', include('application.urls')),
    path('hacker/', include('hacker.urls')),
    path('staff/', include('staff.urls')),
    path('godmode/', include('godmode.urls')),
    path('company/', include('company.urls')),
]

if not settings.DEBUG:

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
