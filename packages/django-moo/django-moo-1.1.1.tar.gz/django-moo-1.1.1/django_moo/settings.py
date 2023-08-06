from django.conf import settings as django_settings

# DJANGO_URL = {}
DJANGO_MOO = {}

def get_setting():
    return getattr(django_settings, 'DJANGO_MOO', {})