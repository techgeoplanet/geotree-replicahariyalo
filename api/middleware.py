import jwt
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.signals import user_logged_out
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

User = get_user_model()

class RequestLimitMiddleware(MiddlewareMixin):
    authenticated_requests = {}  # Class-level dictionary to track authenticated users' requests

    def process_view(self, request, view_func, view_args, view_kwargs):
        try:
            user = self.get_user_from_request(request)

            if user.is_authenticated:
                # Check if user has attributes 'is_staff' and 'is_superuser'
                if hasattr(user, 'is_staff') and hasattr(user, 'is_superuser'):
                    if user.is_staff or user.is_superuser:
                        return  # No limit for staff or superuser/admin users

                # Default behavior for other authenticated users
                user_key = f"user_requests_{user.id}"
                request_limit = settings.AUTHENTICATED_REQUEST_LIMIT
            else:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key
                user_key = f"anon_requests_{session_key}"
                request_limit = settings.ANONYMOUS_REQUEST_LIMIT

            request_count = cache.get(user_key, 0)

            if request_count >= request_limit:
                message = "You have exceeded your maximum allowed requests. Please try again after some time."
                return HttpResponse(
                    f"<h2 style='text-align: center; font-size: 44px; height: 100vh; display: flex; justify-content: center; align-items: center;'>{message}</h2>",
                    status=429,
                    content_type="text/html; charset=utf-8"
                )

            cache.set(user_key, request_count + 1, timeout=settings.REQUEST_TIMEOUT)

        except Exception as e:
            return HttpResponse(
                f"<h2 style='text-align: center; font-size: 44px; height: 100vh; display: flex; justify-content: center; align-items: center;'>Error: {str(e)}</h2>",
                status=500,
                content_type="text/html; charset=utf-8"
            )

    def process_response(self, request, response):
        try:
            user = self.get_user_from_request(request)

            if user.is_authenticated:
                # Check if user has attributes 'is_staff' and 'is_superuser'
                if hasattr(user, 'is_staff') and hasattr(user, 'is_superuser'):
                    if not user.is_staff and not user.is_superuser:
                        user_key = f"user_requests_{user.id}"
                    else:
                        return response  # No need to add request count header for staff or superusers
                else:
                    user_key = f"user_requests_{user.id}"
            else:
                session_key = request.session.session_key
                user_key = f"anon_requests_{session_key}"

            request_count = cache.get(user_key, 0)
            response["X-Request-Count"] = request_count

        except Exception as e:
            response["X-Request-Count"] = f"Error: {str(e)}"

        return response

    def get_user_from_request(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            try:
                jwt_auth = JWTAuthentication()
                validated_token = jwt_auth.get_validated_token(token)
                user = jwt_auth.get_user(validated_token)
                return user
            except (InvalidToken, User.DoesNotExist):
                return AnonymousUser()
        return request.user

def clear_request_count(sender, user, request, **kwargs):
    try:
        if hasattr(user, 'is_staff') and hasattr(user, 'is_superuser'):
            if not (user.is_staff or user.is_superuser):
                user_key = f"user_requests_{user.id}"
                cache.delete(user_key)

        # Remove from the class-level dictionary
        if user.id in RequestLimitMiddleware.authenticated_requests:
            del RequestLimitMiddleware.authenticated_requests[user.id]

    except Exception as e:
        pass  # Handle the error or log it if necessary

user_logged_out.connect(clear_request_count)
