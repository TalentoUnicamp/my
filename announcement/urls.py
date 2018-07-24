from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api

router = DefaultRouter()
router.register(r'announcement', api.AnnouncementViewset)

apipatterns = router.urls

apipatterns += [
]

app_name = 'announcement'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api')
]
