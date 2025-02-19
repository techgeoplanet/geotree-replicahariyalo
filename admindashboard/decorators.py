# myapp/decorators.py
from django.http import JsonResponse
from functools import wraps

def staff_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            if not request.user.is_staff:
                return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        except AttributeError:
            return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        return view_func(request, *args, **kwargs)
    return _wrapped_view
