# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/subscriptions/tickets/<str:unique_id>/<str:signal>/', consumers.TicketSignalConsumer, name='ticket_subscription'),
    path('ws/subscriptions/online_mentor/', consumers.OnlineMentorConsumer, name='online_mentor'),
]
