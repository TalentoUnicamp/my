from rest_framework import views, response
from django.db.models import Case, Count, Q, When
from rest_condition import Or
from settings.models import Settings
from user_profile.models import Profile
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from company.permissions import EmployeeHasAccess
from .util import db_bool


class HackerStats(views.APIView):

    permission_classes = [Or(IsAdmin, IsStaff, EmployeeHasAccess)]

    def get(self, request):
        settings = Settings.get()
        can_confirm = Settings.can_confirm(settings=settings)
        reg_open = Settings.registration_is_open(settings=settings)

        hacker = ~Q(hacker=None)
        checked_in = Q(hacker__checked_in=True)
        confirmed = Q(hacker__confirmed=True)
        withdraw = Q(hacker__withdraw=True)
        waitlist = Q(hacker__waitlist=True)
        admitted = Q(hacker__admitted=True) & ~checked_in & ~confirmed & ~withdraw & ~waitlist
        declined = Q(hacker__declined=True)
        submitted = ~Q(hacker__application=None) & ~admitted
        incomplete = hacker & ~submitted
        unverified = hacker & ~Q(shortcuts__is_verified=True)
        data = Profile.objects.aggregate(
            hackers=Count('pk', filter=hacker),
            checked_in=Count('pk', filter=checked_in),
            confirmed=Count('pk', filter=confirmed),
            withdraw=Case(
                When(
                    db_bool(can_confirm is True),
                    then=Count('pk', filter=withdraw)),
                default=0
            ),
            waitlist=Case(
                When(
                    db_bool(can_confirm is True),
                    then=Count('pk', filter=waitlist)),
                default=0
            ),
            admitted=Case(
                When(
                    db_bool(can_confirm is True),
                    then=Count('pk', filter=admitted)),
                default=0
            ),
            declined=Case(
                When(
                    db_bool(can_confirm is True),
                    then=Count('pk', filter=declined)),
                default=0
            ),
            submitted=Case(
                When(
                    db_bool(can_confirm is True),
                    then=Count('pk', filter=submitted)),
                default=0
            ),
            late=Case(
                When(
                    db_bool(can_confirm is False),
                    then=Count('pk', filter=hacker & ~checked_in & ~admitted)),
                When(
                    db_bool(reg_open is False),
                    then=Count('pk', filter=incomplete)),
                default=0
            ),
            incomplete=Case(
                When(
                    db_bool(reg_open is True),
                    then=Count('pk', filter=incomplete)),
                default=0
            ),
            unverified=Count('pk', filter=unverified)
        )
        return response.Response(data)
