from django.utils.deprecation import MiddlewareMixin


class CaptureRequestInfoMiddleware(MiddlewareMixin):
    """
    Agrega a cada request atributos:
      - client_ip
      - user_agent
    Para que estén disponibles en cualquier vista o signal.
    """
    def process_request(self, request):
        # IP del cliente
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            request.client_ip = x_forwarded_for.split(",")[0]
        else:
            request.client_ip = request.META.get("REMOTE_ADDR")

        # Navegador / dispositivo
        request.user_agent = request.META.get("HTTP_USER_AGENT", "Desconocido")
