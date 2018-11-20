import re

from django.conf import settings
from django.http import HttpResponse

from .models import ApiToken


class ApiTokenAuthenticationMiddleware:
    """Custom authentication middleware which using ApiToken."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not re.match(settings.ZOO_API_URL, request.path):
            return self.get_response(request)

        if request.user.is_authenticated:
            return self.get_response(request)

        auth_header = request.META.get("HTTP_AUTHORIZATION")

        if auth_header is None:
            return HttpResponse("Missing Authorization header for API.", status=401)

        m = re.match(r"Bearer (?P<token>.+)", auth_header)
        if m:
            token = m.group("token")
        else:
            return HttpResponse(
                "Wrong Authorization header value. Expected: 'Bearer <token>'",
                status=401,
            )

        try:
            ApiToken.objects.get(token=token)
        except ApiToken.DoesNotExist:
            return HttpResponse("401: Unauthorized", status=401)

        return self.get_response(request)
