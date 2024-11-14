# middleware.py (inside your Django project)

from django.http import JsonResponse


class CheckFrontendRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request contains the custom header 'X-Requested-By' with value 'frontend'
        if request.path.startswith('/api/') and request.headers.get('X-Requested-By') != 'frontend':
            return JsonResponse({'error': 'Forbidden'}, status=403)  # Block access

        # Proceed with the request if the header is valid
        response = self.get_response(request)
        return response
