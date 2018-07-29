from rest_framework import views, response, generics
from django.db.models import Count, Q
from django.contrib.auth.models import User
from rest_condition import Or
from project.generics import PrefetchListAPIView
from user_profile.models import Profile
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from company.permissions import EmployeeHasAccess
from .serializers import HackerSignupSerializer, HackerApplicationSerializer


class HackerStats(views.APIView):

    permission_classes = [Or(IsAdmin, IsStaff, EmployeeHasAccess)]

    def get(self, request):

        hacker = ~Q(hacker=None)
        checked_in = Q(shortcuts__state='checkedin')
        confirmed = Q(shortcuts__state='confirmed')
        withdraw = Q(shortcuts__state='withdraw')
        waitlist = Q(shortcuts__state='waitlist')
        admitted = Q(shortcuts__state='admitted')
        declined = Q(shortcuts__state='declined')
        submitted = Q(shortcuts__state='submitted')
        incomplete = Q(shortcuts__state='incomplete')
        late = Q(shortcuts__state='late')
        unverified = hacker & Q(shortcuts__state='unverified')
        data = Profile.objects.aggregate(
            hackers=Count('pk', filter=hacker),
            checked_in=Count('pk', filter=checked_in),
            confirmed=Count('pk', filter=confirmed),
            withdraw=Count('pk', filter=withdraw),
            waitlist=Count('pk', filter=waitlist),
            admitted=Count('pk', filter=admitted),
            declined=Count('pk', filter=declined),
            submitted=Count('pk', filter=submitted),
            late=Count('pk', filter=late),
            incomplete=Count('pk', filter=incomplete),
            unverified=Count('pk', filter=unverified)
        )
        return response.Response(data)


class HackerSignupList(generics.ListAPIView):
    serializer_class = HackerSignupSerializer
    permission_classes = [Or(IsAdmin, IsStaff, EmployeeHasAccess)]

    def get_queryset(self):
        return User.objects.exclude(profile__hacker=None).order_by('date_joined')


class HackerApplicationList(PrefetchListAPIView):
    serializer_class = HackerApplicationSerializer
    permission_classes = [Or(IsAdmin, IsStaff, EmployeeHasAccess)]

    def get_queryset(self):
        self.queryset = User.objects.exclude(profile__hacker__application=None).order_by('date_joined')
        return super().get_queryset()
