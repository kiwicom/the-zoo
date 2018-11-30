"""zoo URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="service_list")),
    path("repos/", include("zoo.repos.urls")),
    path("services/", include("zoo.services.urls")),
    path("auditing/", include("zoo.auditing.urls")),
    path("objectives/", include("zoo.objectives.urls")),
    path("analytics/", include("zoo.analytics.urls")),
    path("accounts/", include("allauth.urls")),
    path("silk/", include("silk.urls")),
    path("admin/", admin.site.urls),
    path("graphql", include("zoo.api.urls")),
    path(
        "robots.txt",
        lambda _: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain"),
    ),
    path("ping", lambda _: HttpResponse("200 Pong", content_type="text/plain")),
]


handler404 = "zoo.base.views.not_found"
handler500 = "zoo.base.views.server_error"


if settings.DEBUG:
    import debug_toolbar
    from . import views

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
        path("http404", views.not_found),
        path("http500", views.server_error),
    ] + urlpatterns
