import os

try:
    from django.conf import settings
except ModuleNotFoundError:
    settings = object()

FACEBOOK_LOGIN_BASE_URL = getattr(settings, "FACEBOOK_LOGIN_BASE_URL", "https://facebook.com")

GRAPH_API_BASE_URL = getattr(settings, "GRAPH_API_BASE_URL", "https://graph.facebook.com")

GRAPH_API_VERSION = getattr(settings, "GRAPH_API_VERSION", "v14.0")

GRAPH_API_URL = os.path.join(GRAPH_API_BASE_URL, GRAPH_API_VERSION)

GRAPH_API_REDIRECT_URI = getattr(settings, "GRAPH_API_REDIRECT_URI", "http://localhost:8000")

GRAPH_API_APP_ID = getattr(settings, "GRAPH_API_APP_ID", None)

GRAPH_API_APP_SECRET = getattr(settings, "GRAPH_API_APP_SECRET", None)

FACEBOOK_LOGIN_URL = os.path.join(FACEBOOK_LOGIN_BASE_URL, GRAPH_API_VERSION)

DEFAULT_CHUNK_SIZE = 5
