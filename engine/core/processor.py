from functools import lru_cache
from django.conf import settings
def get_static_version(request):A=settings.STATIC_VERSION;return{'static_version':A}