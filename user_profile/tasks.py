from .emails import verify_email, recover_token_email
from celery import shared_task


@shared_task
def send_verify_email(profile_id):
    from .models import Profile
    profile = Profile.objects.get(id=profile_id)
    return verify_email(profile)


@shared_task
def send_recover_token_email(profile_id):
    from .models import Profile
    profile = Profile.objects.get(id=profile_id)
    return recover_token_email(profile)
