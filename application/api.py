from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from staff.permissions import IsStaff
from .serializers import ApplicationRetrieveSerializer, FormOptionsSerializer
from .models import Application


class ViewApplication(RetrieveAPIView):
    serializer_class = ApplicationRetrieveSerializer
    permission_classes = [IsStaff]
    queryset = Application.objects.all()
    lookup_field = 'hacker__profile__unique_id'
    lookup_url_kwarg = 'unique_id'


class FormOptionsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get_data_list(self, option):
        import csv
        with open(f'application/choices/{option}.csv') as f:
            return {'results': [{k: v for k, v in row.items()}
                                for row in csv.DictReader(f, skipinitialspace=True)]}

    def get(self, request, *args, **kwargs):
        try:
            option = kwargs.get('option')
            data = self.get_data_list(option)
            serializer = FormOptionsSerializer(data=data)
            if serializer.is_valid():
                return Response(serializer.data)
        except FileNotFoundError:
            pass
        serializer = FormOptionsSerializer(data={'success': False, 'results': []})
        serializer.is_valid()
        return Response(serializer.data)
