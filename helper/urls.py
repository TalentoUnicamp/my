from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, api

router = DefaultRouter()
router.register(r'ticket', api.TicketViewset)
router.register(r'mentor', api.MentorViewset)
router.register(r'online_mentors', api.OnlineMentorViewset, 'online_mentors')

apipatterns = router.urls

apipatterns += [
    path('toggle_is_mentor/', api.ToggleIsMentor.as_view(), name='toggle_is_mentor'),
    path('self_mentor/', api.SelfMentor.as_view(), name='self_mentor'),
]

app_name = 'helper'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('', views.HelperView.as_view(), name='index'),
]
