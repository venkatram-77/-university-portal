from .models import UserRole


def current_user_role(request):
    role = 'student'
    user = getattr(request, 'user', None)
    if user is not None and user.is_authenticated:
        try:
            if hasattr(user, 'role'):
                try:
                    if user.role:
                        role = user.role.role
                    elif user.is_superuser:
                        role = 'admin'
                    else:
                        role = 'student'
                except UserRole.DoesNotExist:
                    role = 'admin' if user.is_superuser else 'student'
            elif user.is_superuser:
                role = 'admin'
        except Exception:
            if user.is_superuser:
                role = 'admin'
    return {'current_user_role': role}
