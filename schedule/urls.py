from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api, views, exports

router = DefaultRouter()
router.register('event', api.EventViewset)
router.register('my_events', api.MyEventViewset, 'my_event')
router.register('registered_events', api.RegisteredEventViewset, 'registered_event')
router.register('not_registered_events', api.NotRegisteredEventViewset, 'not_registered_event')
router.register('attended_events', api.AttendedEventViewset, 'attended_event')
router.register('full_events', api.FullEventViewset, 'full_event')
router.register('checkinable_events', api.CheckinableEventViewset, 'checkinable_events')
router.register('my_full_events', api.MyFullEventViewset, 'my_full_event')
router.register('feedback', api.FeedbackViewset)

apipatterns = router.urls

apipatterns += [
    path('attend_event/', api.AttendEvent.as_view(), name="attend_event"),
    path('neglect_event/', api.NeglectEvent.as_view(), name="neglect_event"),
    path('fetch_checkin/', api.FetchCheckinAttendee.as_view(), name="fetch_checkin"),
    path('checkin/', api.CheckinAttendee.as_view(), name="checkin")
]

exportrouter = DefaultRouter()
exportrouter.register('events', exports.ExportEventsViewset, 'events')

exportpatterns = exportrouter.urls

exportpatterns += [
    path('feedback/<str:event_id>/', exports.ExportFeedback.as_view(), name="feedback"),
]

app_name = 'schedule'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('exports/', include((exportpatterns, 'exports')), name='exports'),
    path('', views.ScheduleView.as_view(), name='index')
]
