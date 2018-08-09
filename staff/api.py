from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils.crypto import get_random_string
from rest_framework import views
from godmode.permissions import IsAdmin
from user_profile.models import Profile
from hacker.models import Hacker
from .permissions import IsStaff
from .models import Staff


class ToggleIsStaff(views.APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        unique_id = request.data['unique_id']
        profile = Profile.objects.get(unique_id=unique_id)
        if profile.is_staff:
            profile.staff.delete()
            profile.trigger_update()
        else:
            staff = Staff(profile=profile)
            staff.save()
        return views.Response({'message': 'Permissão alterada'})


class CreateBlankHacker(views.APIView):
    permission_classes = [IsStaff]

    def uniqueUsername(self):
        username = get_random_string(length=20)
        if User.objects.filter(username=username).exists():
            return self.uniqueUsername()
        return username

    def post(self, request):
        user = User(username=self.uniqueUsername())
        user.save()
        hacker = Hacker(profile=user.profile)
        hacker.save()
        url = request.build_absolute_uri('/').strip("/") + reverse('profile:token_login', args={user.profile.token})
        return views.Response({'token': user.profile.token, 'url': url})
