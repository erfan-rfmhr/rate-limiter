from django.core.exceptions import ValidationError, ObjectDoesNotExist, PermissionDenied
from rest_framework import exceptions
from django.http import Http404
from rest_framework.views import set_rollback, Response


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*(exc.args))
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*(exc.args))
    elif isinstance(exc, ValidationError):
        exc = exceptions.ValidationError(*(exc.args))
    elif isinstance(exc, ObjectDoesNotExist):
        exc = exceptions.NotFound(*(exc.args))

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, "auth_header", None):
            headers["WWW-Authenticate"] = exc.auth_header
        if getattr(exc, "wait", None):
            headers["Retry-After"] = "%d" % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {"detail": exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None
