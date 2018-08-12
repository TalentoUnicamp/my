from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.auth import login
from django.conf import settings
from django.db.models import Q
from django.db import connection
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import views, response
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from project.generics import PrefetchListAPIView
from .models import Profile, User
from .tasks import send_recover_token_email
from .serializers import ListProfileSerializer, ListHackerProfileSerializer, SUIProfileListSerializer
import time


class CheckToken(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('token')
        try:
            instance = Profile.objects.get(token=token)
            login(request, instance.user)
            return views.Response({'redirect_url': request.GET.get('next', settings.PROFILE_REDIRECT_URL)})
        except Profile.DoesNotExist:
            time.sleep(2)
            return views.Response({'error': 'Token inválido'}, status=404)


class ResetTokenEmail(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            user.profile.new_token()
            send_recover_token_email.delay(user.profile.id)
        time.sleep(2)
        return views.Response({'message': 'Olhe seu email :)'})


class ChangeEmail(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        user = request.user
        user.profile.change_email(email)
        time.sleep(2)
        return views.Response({'message': 'Olhe seu email :)'})


class ChangeToken(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = user.profile.new_token()
        return views.Response({'message': 'Token alterado', 'token': token})


class ListProfiles(PrefetchListAPIView):
    serializer_class = ListProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAdmin]


class ListHackerProfiles(PrefetchListAPIView):
    serializer_class = ListHackerProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsStaff]

    def get_queryset(self):
        self.queryset = self.queryset.filter(shortcuts__state__in=['checkedin', 'confirmed', 'waitlist', 'admitted', 'submitted', 'declined'])
        return super().get_queryset()


class SUIListProfiles(PrefetchListAPIView):
    serializer_class = SUIProfileListSerializer
    queryset = Profile.objects.filter(shortcuts__is_verified=True)
    permission_classes = [IsStaff]

    def get_queryset(self, *args, **kwargs):
        q = self.request.query_params.get('search', None)
        queryset = self.queryset
        if q:
            if connection.vendor == 'postgresql':
                query = SearchQuery(q, config="portuguese")
                vectors = SearchVector('shortcuts__full_name', config="portuguese", weight="A") + SearchVector('user__email', config="portuguese", weight="B") + SearchVector('unique_id', config="portuguese", weight="C")
                queryset = queryset.annotate(
                    search=vectors
                ).filter(
                    Q(shortcuts__full_name__icontains=q) |
                    Q(user__email__icontains=q) |
                    Q(unique_id__icontains=q) |
                    Q(search=query)
                ).annotate(
                    rank=SearchRank(vectors, query)
                ).order_by(
                    '-rank'
                )
            else:
                queryset = queryset.filter(
                    Q(shortcuts__full_name__icontains=q) |
                    Q(user__email__icontains=q) |
                    Q(unique_id__icontains=q)
                )
        self.queryset = queryset
        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset(*args, **kwargs))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        success = True
        if len(serializer.data) == 0:
            success = False
        return response.Response({'success': success, 'results': serializer.data})
