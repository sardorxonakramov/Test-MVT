from django.core.exceptions import PermissionDenied

def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'teacher':
            raise PermissionDenied("Only teachers are allowed.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
