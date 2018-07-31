from django.urls import path, include
from . import api, exports

apipatterns = [
    path('confirm/', api.ConfirmPresence.as_view(), name='confirm'),
    path('withdraw/', api.Withdraw.as_view(), name='withdraw'),
    path('undo_withdraw/', api.UndoWithdraw.as_view(), name='undo_withdraw'),
    path('toggle_is_hacker/', api.ToggleIsHacker.as_view(), name='toggle_is_hacker'),

    path('admit_hacker/', api.Admit.as_view(), name='admit_hacker'),
    path('decline_hacker/', api.Decline.as_view(), name='decline_hacker'),
    path('unwaitlist_hacker/', api.Unwaitlist.as_view(), name='unwaitlist_hacker'),

    path('fetch_checkin_hacker/', api.FetchCheckinHacker.as_view(), name='fetch_checkin_hacker'),
    path('checkin_hacker/', api.CheckinHacker.as_view(), name='checkin_hacker'),
]

exportpatterns = [
    path('scanned_hackers/', exports.ExportScannedHackers.as_view(), name="scanned_hackers"),
    path('all_hackers/', exports.ExportAllHackers.as_view(), name="all_hackers"),
]

app_name = 'hacker'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api'),
    path('exports/', include((exportpatterns, 'exports')), name='exports')
]
