from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from rest_framework import views, generics
from user_profile.models import Profile
from user_profile.tasks import send_verify_email
from .permissions import IsAdmin


class ToggleIsAdmin(views.APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        unique_id = request.data['unique_id']
        user = Profile.objects.get(unique_id=unique_id).user
        user.is_superuser = not user.is_superuser
        user.save()
        return views.Response({'message': 'Permissão alterada'})


class DeleteUser(generics.DestroyAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    lookup_field = 'profile__unique_id'
    lookup_url_kwarg = 'unique_id'


class BatchCreateUsers(views.APIView):
    permission_classes = [IsAdmin]

    def uniqueUsername(self):
        username = get_random_string(length=20)
        if User.objects.filter(username=username).exists():
            return self.uniqueUsername()
        return username

    def post(self, request):
        users = request.data['users']
        send_emails = request.data['send_emails']

        for user in users:

            if User.objects.filter(email=user['email']).exists():
                user['result'] = 'error'
                continue

            user.pop('result')
            user.pop('token')

            new = User(**user)
            new.username = self.uniqueUsername()
            new.save()

            user['result'] = 'success'
            user['token'] = new.profile.token

            if send_emails:
                send_verify_email.delay(new.profile.id)
            else:
                profile = new.profile
                profile.verified = True
                profile.save()

        return views.Response({'users': users})
