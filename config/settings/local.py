# ruff: noqa: E501
from .base import *  # noqa: F403
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import env

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="PUQpP75TH8wYMB3MpL7lZGQvyiyKdcIv2KhuJgjMUiEmO4PEFEwA5h2fjw1MRaao",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]  # noqa: S104
ALLOWED_HOSTS += [
    '192.168.28.112',
    '192.168.10.6',
    '192.168.1.2',
]

CSRF_TRUSTED_ORIGINS = [
    'http://192.168.10.6',
    'http://192.168.1.2',
]

CORS_ALLOWED_ORIGINS = [
    'http://192.168.10.6',
    'http://192.168.1.2',
]
# CACHES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    },
}

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend",
)

# WhiteNoise
# ------------------------------------------------------------------------------
# http://whitenoise.evans.io/en/latest/django.html#using-whitenoise-in-development
INSTALLED_APPS = ["whitenoise.runserver_nostatic", *INSTALLED_APPS]


# django-debug-toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]
INSTALLED_APPS += ["silk"]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
MIDDLEWARE += ['silk.middleware.SilkyMiddleware',]
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
        # Disable profiling panel due to an issue with Python 3.12:
        # https://github.com/jazzband/django-debug-toolbar/issues/1875
        "debug_toolbar.panels.profiling.ProfilingPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#internal-ips
INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
if env("USE_DOCKER") == "yes":
    import socket

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS += [".".join(ip.split(".")[:-1] + ["1"]) for ip in ips]
    # RunServerPlus
    # ------------------------------------------------------------------------------
    # This is a custom setting for RunServerPlus to fix reloader issue in Windows docker environment
    # Werkzeug reloader type [auto, watchdog, or stat]
    RUNSERVERPLUS_POLLER_RELOADER_TYPE = 'stat'
    # If you have CPU and IO load issues, you can increase this poller interval e.g) 5
    RUNSERVERPLUS_POLLER_RELOADER_INTERVAL = 1

# django-extensions
# ------------------------------------------------------------------------------
# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions"]

# Your stuff...
# ------------------------------------------------------------------------------
SILKY_PYTHON_PROFILER = True
# SILKY_PYTHON_PROFILER_BINARY = True

SILKY_AUTHENTICATION = True
# SILKY_AUTHORISATION = True

SILKY_MAX_REQUEST_BODY_SIZE = -1
SILKY_MAX_RESPONSE_BODY_SIZE = 1024
SILKY_INTERCEPT_PERCENT = 50

SILKY_MAX_RECORDED_REQUESTS = 10**4
SILKY_MAX_RECORDED_REQUESTS_CHECK_PERCENT = 10

SILKY_DYNAMIC_PROFILING = [{
    'module': 'core.mqc.views',
    'function': 'MajorQualityCaseFilterListView.post',
}]