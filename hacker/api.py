from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_condition import Or, And
from settings.permissions import CanConfirm
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from user_profile.models import Profile
from .permissions import IsAdmitted, IsWithdraw, IsConfirmed
from .models import Hacker


class ConfirmPresence(views.APIView):

    permission_classes = [And(IsAdmitted, CanConfirm)]

    def post(self, request):
        hacker = request.user.profile.hacker
        hacker.confirm()
        return views.Response({'message': 'Presença confirmada', 'state': hacker.profile.state})


class Withdraw(views.APIView):

    permission_classes = [Or(IsAdmitted, IsConfirmed)]

    def post(self, request):
        hacker = request.user.profile.hacker
        hacker.withdraw_from_event()
        return views.Response({'message': 'Desistência completa', 'state': hacker.profile.state})


class UndoWithdraw(views.APIView):

    permission_classes = [And(IsWithdraw, CanConfirm)]

    def post(self, request):
        hacker = request.user.profile.hacker
        hacker.admit(False)
        return views.Response({'message': 'Desistência desfeita', 'state': hacker.profile.state})


class Admit(views.APIView):

    permission_classes = [IsStaff]

    def post(self, request):
        unique_id = request.data.get('unique_id')
        hacker = get_object_or_404(Hacker, profile__unique_id=unique_id)
        if hacker.profile.state not in ['submitted', 'declined']:
            return views.Response({'message': 'State is not submitted or declined'}, status=400)
        hacker.admit()
        return views.Response({'message': 'Hacker admitido'})


class Decline(views.APIView):

    permission_classes = [IsStaff]

    def post(self, request):
        unique_id = request.data.get('unique_id')
        hacker = get_object_or_404(Hacker, profile__unique_id=unique_id)
        if hacker.profile.state not in ['submitted', 'admitted', 'confirmed']:
            return views.Response({'message': "State is not in 'submitted', 'admitted', 'confirmed'"}, status=400)
        hacker.decline()
        return views.Response({'message': 'Hacker rejeitado'})


class Unwaitlist(views.APIView):

    permission_classes = [IsStaff]

    def post(self, request):
        unique_id = request.data.get('unique_id')
        hacker = get_object_or_404(Hacker, profile__unique_id=unique_id)
        if hacker.profile.state != 'waitlist':
            return views.Response({'message': "State is not waitlist"}, status=400)
        hacker.unwaitlist(True)
        return views.Response({'message': 'Hacker tirado da fila'})


class ToggleIsHacker(views.APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        unique_id = request.data['unique_id']
        profile = Profile.objects.get(unique_id=unique_id)
        if profile.is_hacker:
            profile.hacker.delete()
        else:
            hacker = Hacker(profile=profile)
            hacker.save()
        return views.Response({'message': 'Permissão alterada'})


class FetchCheckinHacker(views.APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        unique_id = request.data['unique_id']
        try:
            profile = Profile.objects.get(unique_id=unique_id)
        except Profile.DoesNotExist:
            return views.Response({
                'title': 'Usuário não existe!',
                'message': 'Não foi possível encontrar um usuário válido com esse código',
                'status': 'error'
            })
        if not profile.is_hacker:
            return views.Response({
                'title': 'Usuário não é hacker!',
                'message': 'Esse usuário é válido, mas não é um hacker',
                'status': 'error'
            })
        if profile.state == 'checkedin':
            return views.Response({
                'title': 'Hacker já fez Check-In!',
                'message': 'Hackers só podem fazer check-in uma vez',
                'status': 'error'
            })
        if profile.state != 'confirmed':
            return views.Response({
                'title': 'Hacker não está confirmado!',
                'message': 'Apenas hackers que confirmaram presença podem fazer check-in',
                'status': 'error'
            })

        return views.Response({
            'title': f'{profile.full_name}',
            'message': f'Deseja fazer o check-in de {profile.full_name}?',
            'status': 'success'
        })


class CheckinHacker(views.APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        unique_id = request.data['unique_id']
        profile = get_object_or_404(Profile, unique_id=unique_id)
        if not profile.state == 'confirmed':
            return views.Response({'error': 'Invalid hacker ID'}, status=400)
        hacker = profile.hacker
        hacker.check_in()
        return views.Response({'message': 'Check-In complete'})
