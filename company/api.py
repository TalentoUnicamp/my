from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views, mixins
from godmode.permissions import IsAdmin
from user_profile.models import Profile
from .permissions import IsAdminOrEmployeeReadOnly, EmployeeHasAccess
from .serializers import CompanySerializer, ReadEmployeeSerializer, CreateEmployeeSerializer, ScanSerializer
from .models import Company, Employee, Scan


class CompanyViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrEmployeeReadOnly]
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class EmployeeViewset(
        mixins.RetrieveModelMixin,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    permission_classes = [IsAdmin]
    queryset = Employee.objects.all()
    lookup_field = 'profile__unique_id'

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return ReadEmployeeSerializer
        return CreateEmployeeSerializer


class ScanViewset(
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        viewsets.GenericViewSet):
    permission_classes = [EmployeeHasAccess]
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    def get_queryset(self):
        return self.queryset.filter(scanner__employee__company=self.request.user.profile.employee.company)


class FetchScanHacker(views.APIView):
    permission_classes = [EmployeeHasAccess]

    def post(self, request):
        unique_id = request.data['unique_id']
        try:
            profile = Profile.objects.get(unique_id=unique_id)
        except Profile.DoesNotExist:
            return views.Response({
                'title': 'Usuário não existe!',
                'message': 'Não foi possível encontrar um usuário válido com esse código'
            }, status=400)
        scanner = request.user.profile
        if not profile.is_hacker:
            return views.Response({
                'title': 'Usuário não é um participante!',
                'message': 'Esse usuário é válido, mas não é um participante',
            }, status=400)
        if profile.state != 'checkedin':
            return views.Response({
                'title': 'Participante não fez check-in!',
                'message': 'Apenas participantes que fizeram o check-in podem ser escaneados',
            }, status=400)
        if profile.scanned_me.filter(scanner__employee__company__id=scanner.employee.company.id).exists():
            return views.Response({
                'title': 'Participante já escaneado!',
                'message': 'Sua empresa já escaneou esse participante',
            }, status=400)
        return views.Response({
            'title': f'{profile.full_name}',
            'message': f'Deseja escanear {profile.full_name}?',
        })


class ScanHacker(views.APIView):
    permission_classes = [EmployeeHasAccess]

    def post(self, request):
        unique_id = request.data['unique_id']
        scanner = request.user.profile
        profile = get_object_or_404(Profile, unique_id=unique_id)
        if not profile.state == 'checkedin':
            return views.Response({'error': 'Invalid hacker ID'}, status=400)
        if profile.scanned_me.filter(scanner__employee__company__id=scanner.employee.company.id).exists():
            return views.Response({'error': 'Hacker already scanned'}, status=400)

        scan = Scan(scanner=scanner, scannee=profile)
        scan.save()
        return views.Response({'message': 'Scan complete', 'id': scan.id, 'name': profile.full_name})
