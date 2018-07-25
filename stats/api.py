from rest_framework import views, response
from django.db.models import Count, Q
from rest_condition import Or
from user_profile.models import Profile
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from company.permissions import EmployeeHasAccess


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
