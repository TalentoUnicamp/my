from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from project.mixins import PrefetchQuerysetModelMixin
from rest_condition import Or, And
from project.permissions import IsReadyOnlyRequest
from godmode.permissions import IsAdmin
from .serializers import AnnouncementSerializer
from .models import Announcement


class AnnouncementViewset(
        PrefetchQuerysetModelMixin,
        viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [Or(IsAdmin, And(IsAuthenticated, IsReadyOnlyRequest))]
    queryset = Announcement.objects.all().order_by('-created')
