from rest_framework.generics import RetrieveUpdateAPIView
from godmode.permissions import IsAdmin
from .serializers import SettingsSerializer
from .models import Settings


class SettingsView(RetrieveUpdateAPIView):
    serializer_class = SettingsSerializer
    permission_classes = [IsAdmin]

    def get_object(self):
        queryset = Settings.get()
        return queryset
