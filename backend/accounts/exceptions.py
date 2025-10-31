# accounts/exceptions.py
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

def exception_handler(exc, context):
    """
    Envuelve todas las respuestas de error en un formato coherente:
    {
      "detail": "...",
      "code": "bad_request|permission_denied|validation_error|server_error",
      "errors": {...}  # solo cuando hay campos
    }
    """
    resp = drf_exception_handler(exc, context)
    if resp is None:
        return Response({
            "detail": "Ha ocurrido un error interno.",
            "code": "server_error",
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    payload = {"detail": "", "code": "",}
    status_code = resp.status_code

    if status_code == 400:
        payload["code"] = "bad_request"
    elif status_code == 401:
        payload["code"] = "unauthorized"
    elif status_code == 403:
        payload["code"] = "permission_denied"
    elif status_code == 404:
        payload["code"] = "not_found"
    elif status_code == 429:
        payload["code"] = "too_many_requests"
    else:
        payload["code"] = "error"

    data = resp.data

    if isinstance(data, dict):
        detail = data.get("detail")
        if isinstance(detail, (str,)):
            payload["detail"] = detail
        else:
            payload["detail"] = "Solicitud inválida." if status_code == 400 else payload["code"].replace("_"," ").title()

        field_errors = {k: v for k, v in data.items() if k != "detail"}
        if field_errors:
            payload["errors"] = field_errors
    else:
        payload["detail"] = str(data)

    return Response(payload, status=status_code)
