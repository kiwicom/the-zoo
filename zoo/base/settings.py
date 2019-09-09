"""Django settings for zoo project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from pathlib import Path

import environ

from . import logs
from ..utils import _get_app_version

version = _get_app_version()

root = Path(__file__).parents[1]
env = environ.Env(
    ZOO_DEBUG=(bool, False),
    ZOO_CELERY_BROKER_URL=(str, "redis://redis/0"),
    ZOO_REDIS_CACHE_URL=(str, "redis://redis/1"),
    ZOO_REDBEAT_REDIS_URL=(str, "redis://redis/2"),
    ZOO_DATABASE_OPTIONS=(dict, {}),
    ZOO_DATADOG_API_KEY=(str, None),
    ZOO_DATADOG_APP_KEY=(str, None),
    ZOO_SLACK_URL=(str, None),
    ZOO_GITHUB_TOKEN=(str, None),
    ZOO_GITLAB_URL=(str, None),
    ZOO_GITLAB_TOKEN=(str, None),
    ZOO_GITLAB_DB_URL=(str, None),
    ZOO_USER_AGENT=(str, "zoo/{version}" if version else "zoo"),
    ZOO_PAGERDUTY_TOKEN=(str, None),
    ZOO_PINGDOM_EMAIL=(str, None),
    ZOO_PINGDOM_PASS=(str, None),
    ZOO_PINGDOM_APP_KEY=(str, None),
    ZOO_SENTRY_URL=(str, None),
    ZOO_SENTRY_ORGANIZATION=(str, None),
    ZOO_SENTRY_API_KEY=(str, None),
    ZOO_AUDITING_CHECKS=(list, []),
    ZOO_AUDITING_DROP_ISSUES=(int, 7),
    ZOO_SONARQUBE_URL=(str, None),
    ZOO_SONARQUBE_TOKEN=(str, None),
)

SITE_ROOT = str(root)

DEBUG = env("ZOO_DEBUG")

GA_TRACKING_ID = env("GA_TRACKING_ID", default=None)
GITLAB_URL = env("ZOO_GITLAB_URL")

USER_AGENT = env("ZOO_USER_AGENT").format(version=version)

DATABASES = {
    "default": env.db(default="postgres://postgres:postgres@postgres/postgres")
}
DATABASES["default"]["OPTIONS"] = env("ZOO_DATABASE_OPTIONS")

public_root = root / "public"

MEDIA_ROOT = str(public_root / "media")
MEDIA_URL = "/media/"
STATIC_ROOT = str(public_root / "static")
STATIC_URL = "/static/"
ZOO_CHECKLISTS_ROOT = root / "checklists" / "steps"
ZOO_AUDITING_ROOT = root / "auditing" / "standards"

SECRET_KEY = env("SECRET_KEY", default="mucho secretto")

ALLOWED_HOSTS = ["*"]  # allow any, since the host is validated on the load balancer

INTERNAL_IPS = [
    "127.0.0.1",  # localhost
    "172.18.0.1",  # Docker host IP from inside container (not sure if always)
]

INSTALLED_APPS = [
    "graphene_django",
    "zoo.base.apps.BaseConfig",
    "zoo.auditing.apps.AuditingConfig",
    "zoo.checklists.apps.ChecklistsConfig",
    "zoo.repos.apps.ReposConfig",
    "zoo.services.apps.ServicesConfig",
    "zoo.libraries.apps.LibrariesConfig",
    "zoo.analytics.apps.AnalyticsConfig",
    "zoo.objectives.apps.ObjectivesConfig",
    "zoo.api.apps.ApiConfig",
    "zoo.pagerduty.apps.PagerdutyConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.gitlab",
    "django_extensions",
    "debug_toolbar",
    "raven.contrib.django.raven_compat",
    "stronghold",
    "silk",
    "djangoql",
    "ddtrace.contrib.django",
]

DATADOG_TRACE = {"DEFAULT_SERVICE": "zoo", "TAGS": {"env": "production"}}

SILKY_INTERCEPT_PERCENT = 100 if DEBUG else 0
SILKY_AUTHENTICATION = True
SILKY_AUTHORISATION = True

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware",
    "silk.middleware.SilkyMiddleware",
    "stronghold.middleware.LoginRequiredMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "zoo.api.middleware.ApiTokenAuthenticationMiddleware",
]

ROOT_URLCONF = "zoo.base.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "zoo.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",  # for /admin
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_ADAPTER = "zoo.base.accounts.NoSignupAccountAdapter"
ACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_ADAPTER = "zoo.base.accounts.OpenSignupSocialAccountAdapter"
SOCIALACCOUNT_PROVIDERS = {"gitlab": {"GITLAB_URL": GITLAB_URL, "SCOPE": ["read_user"]}}
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

GRAPHENE = {"SCHEMA": "zoo.api.schema.schema"}

ZOO_API_URL = r"^/graphql$"

STRONGHOLD_PUBLIC_URLS = (
    r"^/admin.*?$",  # let Django manage auth for /admin
    r"^/accounts/login/$",
    r"^/accounts/gitlab.*?$",
    r"^/accounts/social/signup/$",
    r"^/robots.txt$",
    r"^/ping$",
    ZOO_API_URL,
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

RAVEN_CONFIG = {"release": version}

CELERY_BROKER_URL = env("ZOO_CELERY_BROKER_URL")
CELERY_REDBEAT_REDIS_URL = env("ZOO_REDBEAT_REDIS_URL")
REDIS_CACHE_URL = env("ZOO_REDIS_CACHE_URL")
DATADOG_API_KEY = env("ZOO_DATADOG_API_KEY")
DATADOG_APP_KEY = env("ZOO_DATADOG_APP_KEY")
GITLAB_TOKEN = env("ZOO_GITLAB_TOKEN")
GITLAB_DB_URL = env("ZOO_GITLAB_DB_URL")
PAGERDUTY_TOKEN = env("ZOO_PAGERDUTY_TOKEN")
PINGDOM_EMAIL = env("ZOO_PINGDOM_EMAIL")
PINGDOM_PASS = env("ZOO_PINGDOM_PASS")
PINGDOM_APP_KEY = env("ZOO_PINGDOM_APP_KEY")
SLACK_URL = env("ZOO_SLACK_URL")
SENTRY_URL = env("ZOO_SENTRY_URL")
SENTRY_ORGANIZATION = env("ZOO_SENTRY_ORGANIZATION")
SENTRY_API_KEY = env("ZOO_SENTRY_API_KEY")
GITHUB_TOKEN = env("ZOO_GITHUB_TOKEN")
SONARQUBE_URL = env("ZOO_SONARQUBE_URL")
SONARQUBE_TOKEN = env("ZOO_SONARQUBE_TOKEN")

ZOO_AUDITING_CHECKS = env("ZOO_AUDITING_CHECKS")
ZOO_AUDITING_DROP_ISSUES = env("ZOO_AUDITING_DROP_ISSUES")

logs.configure_structlog(DEBUG)
