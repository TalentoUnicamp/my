from rest_framework import viewsets
from project.mixins import PrefetchQuerysetModelMixin
from rest_condition import Or
from godmode.permissions import IsAdmin
from user_profile.permissions import UserReadOnly
from .serializers import AnnouncementSerializer
from .models import Announcement


class AnnouncementViewset(
        PrefetchQuerysetModelMixin,
        viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [Or(IsAdmin, UserReadOnly)]
    queryset = Announcement.objects.all().order_by('-created')
