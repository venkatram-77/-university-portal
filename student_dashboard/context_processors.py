from .models import UserRole


def current_user_role(request):
    role = 'student'
    try:
        if request.user.is_authenticated:
            if hasattr(request.user, 'role') and request.user.role:
                role = request.user.role.role
            elif request.user.is_superuser:
                role = 'admin'
    except Exception:
        if getattr(request.user, 'is_superuser', False):
            role = 'admin'
    return {'current_user_role': role}
