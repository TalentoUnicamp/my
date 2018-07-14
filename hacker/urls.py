from django.urls import path, include
from . import api

apipatterns = [
    path('confirm/', api.ConfirmPresence.as_view(), name='confirm'),
    path('withdraw/', api.Withdraw.as_view(), name='withdraw'),
    path('undo_withdraw/', api.UndoWithdraw.as_view(), name='undo_withdraw'),
    path('list_hackers/', api.ListHackersView.as_view(), name='list_hackers'),
]

app_name = 'hacker'
urlpatterns = [
    path('api/', include((apipatterns, 'api')), name='api')
]
