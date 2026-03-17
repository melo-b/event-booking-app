import logging
import uuid
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class StandardizedExceptionMiddleware:
    """
    Catches unhandled exceptions globally, logs them with a unique trace ID, 
    and returns a standardized JSON response for API clients.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This code runs before the view is called
        response = self.get_response(request)
        # This code runs after the view is called
        return response

    def process_exception(self, request, exception):
        # 1. Generate a unique tracking ID for this specific crash
        error_id = uuid.uuid4().hex

        # 2. Log the critical details securely on the server side (never to the user)
        # exc_info=True captures the full stack trace in your server logs
        logger.error(
            f"Unhandled Exception [ID: {error_id}] | "
            f"Path: {request.path} | Method: {request.method} | "
            f"Error: {str(exception)}",
            exc_info=True
        )

        # 3. Check if the request expects JSON (like a frontend fetch/Axios call)
        # We also check if it's an API route. If so, return our clean JSON schema.
        if request.headers.get('accept') == 'application/json' or request.path.startswith('/api/'):
            payload = {
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected system error occurred. Our engineering team has been notified.",
                    "reference_id": error_id
                }
            }
            return JsonResponse(payload, status=500)

        # 4. If it's a standard web browser request, return None. 
        # This tells Django to fall back to your standard 500.html template.
        return None