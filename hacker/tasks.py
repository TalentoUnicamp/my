from .emails import notify_admitted, nag_admitted, notify_decline, notify_waitlist, notify_unwaitlist
from celery import shared_task


@shared_task
def send_notify_admitted(hacker_id):
    from .models import Hacker
    profile = Hacker.objects.get(id=hacker_id)
    return notify_admitted(profile)


@shared_task
def send_nag_admitted(hacker_id):
    from .models import Hacker
    profile = Hacker.objects.get(id=hacker_id)
    return nag_admitted(profile)


@shared_task
def send_notify_decline(hacker_id):
    from .models import Hacker
    profile = Hacker.objects.get(id=hacker_id)
    return notify_decline(profile)


@shared_task
def send_notify_waitlist(hacker_id):
    from .models import Hacker
    profile = Hacker.objects.get(id=hacker_id)
    return notify_waitlist(profile)


@shared_task
def send_notify_unwaitlist(hacker_id):
    from .models import Hacker
    profile = Hacker.objects.get(id=hacker_id)
    return notify_unwaitlist(profile)
