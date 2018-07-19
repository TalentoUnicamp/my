from rest_framework.generics import RetrieveAPIView
from staff.permissions import IsStaff
from .serializers import ApplicationRetrieveSerializer
from .models import Application


class ViewApplication(RetrieveAPIView):
    serializer_class = ApplicationRetrieveSerializer
    permission_classes = [IsStaff]
    queryset = Application.objects.all()
    lookup_field = 'hacker__profile__unique_id'
    lookup_url_kwarg = 'unique_id'
