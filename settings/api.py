from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from .serializers import SettingsSerializer
from .models import Settings


class SettingsView(RetrieveUpdateAPIView):
    serializer_class = SettingsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        queryset = Settings.get()
        return queryset
