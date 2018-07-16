import os
import django
from channels.routing import get_default_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

application = get_default_application()
application = DjangoWhiteNoise(application)
