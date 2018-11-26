from django.template.response import TemplateResponse


def not_found(request, exception=None):
    """404 error handler which includes ``request`` in the context."""
    return TemplateResponse(
        request, "status/404.html", {"request": request}, status=404
    )


def server_error(request):
    """500 error handler which includes ``request`` in the context."""
    return TemplateResponse(
        request, "status/500.html", {"request": request}, status=500
    )
