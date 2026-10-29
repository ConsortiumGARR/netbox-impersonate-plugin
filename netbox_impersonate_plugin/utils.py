from django.contrib.auth import get_user_model


def allow_impersonate(request):
    return request.user.is_superuser


def impersonable_users(request):
    return get_user_model().objects.filter(is_active=True).order_by("pk")
