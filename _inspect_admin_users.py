from django.contrib.auth import get_user_model


User = get_user_model()

for user in User.objects.filter(is_superuser=True).order_by("id"):
    print(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
            "password_hash": user.password,
        }
    )
