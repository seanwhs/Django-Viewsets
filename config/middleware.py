# config/middleware.py
import logging
import time

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('api.requests')


class DRFRequestResponseLoggingMiddleware(MiddlewareMixin):
    """
    Logs method, path, status, duration and user for all /api/ requests,
    including swagger (/api/docs), schema (/api/schema) and JWT endpoints.
    """

    def process_request(self, request):
        if request.path.startswith('/api/'):
            request._api_start_time = time.monotonic()

    def process_response(self, request, response):
        if request.path.startswith('/api/'):
            duration_ms = None
            start = getattr(request, '_api_start_time', None)
            if start is not None:
                duration_ms = int((time.monotonic() - start) * 1000)

            user = getattr(request, 'user', None)
            user_repr = (
                f'{user.id}:{user.username}'
                if getattr(user, 'is_authenticated', False)
                else 'anonymous'
            )

            logger.info(
                '%s %s -> %s (%s) %sms',
                request.method,
                request.path,
                response.status_code,
                user_repr,
                duration_ms if duration_ms is not None else '-',
            )
        return response