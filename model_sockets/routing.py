# chat/routing.py
from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/subscriptions/models/<str:app>/<str:model>/<str:signal>/', consumers.ModelSignalConsumer, name='model_subscription'),
    path('ws/subscriptions/instances/me/<str:signal>/', consumers.SelfSignalConsumer, name='self_subscription'),
]
