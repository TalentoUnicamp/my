from django.urls import path, include
from . import api

apipatterns = [
    path('confirm/', api.ConfirmPresence.as_view(), name='confirm'),
    path('withdraw/', api.Withdraw.as_view(), name='withdraw'),
    path('undo_withdraw/', api.UndoWithdraw.as_view(), name='undo_withdraw'),
    path('toggle_is_hacker/', api.ToggleIsHacker.as_view(), name='toggle_is_hacker'),

    path('fetch_checkin_hacker/', api.FetchCheckinHacker.as_view(), name='fetch_checkin_hacker'),
    path('checkin_hacker/', api.CheckinHacker.as_view(), name='checkin_hacker'),
]

app_name = 'hacker'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api')
]
