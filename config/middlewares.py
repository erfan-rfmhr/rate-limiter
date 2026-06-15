import logging


class APILoggingMiddleware:
    def __init__(self, get_response):
        self.logger = logging.getLogger("api_request")
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        self.logger.info(
            f"{request.method} {request.path} | Response: {response.status_code}"
        )

        return response
