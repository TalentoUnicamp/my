from rest_framework import viewsets
from project.mixins import PrefetchListModelMixin
from godmode.permissions import IsAdminOrUserReadOnly
from .serializers import AnnouncementSerializer
from .models import Announcement


class AnnouncementViewset(
        PrefetchListModelMixin,
        viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAdminOrUserReadOnly]
    queryset = Announcement.objects.all().order_by('-created')
