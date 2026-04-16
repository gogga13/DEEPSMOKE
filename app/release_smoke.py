import os
import sys
from datetime import timedelta
from pathlib import Path
from uuid import uuid4

import django
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
django.setup()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app import views
from app_web.models import Category, Order, PasswordResetCode, Product, ProductVariant, Profile, Review


User = get_user_model()


def main():
    suffix = uuid4().hex[:8]
    username = f"smoke_{suffix}"
    email = f"{username}@example.com"
    password = "SmokePass123!"
    new_password = "SmokePass456!"
    sent_payload = {}

    # registration
    client = Client()
    signup_response = client.post(
        reverse("account_signup"),
        {
            "username": username,
            "email": email,
            "phone_number": "+380501234567",
            "password1": password,
            "password2": password,
        },
        follow=False,
    )
    print("SIGNUP_STATUS", signup_response.status_code, signup_response.headers.get("Location"))

    user = User.objects.get(username=username)
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.phone = "+380501234567"
    profile.city = "Миколаїв"
    profile.address = "Відділення №1"
    profile.birth_date = timezone.localdate() - timedelta(days=365 * 25)
    profile.save(update_fields=["phone", "city", "address", "birth_date"])

    logout_response = client.post(reverse("account_logout"), follow=False)
    print("LOGOUT_POST_STATUS", logout_response.status_code, logout_response.headers.get("Location"))

    login_response = client.post(reverse("account_login"), {"login": username, "password": password}, follow=False)
    print("LOGIN_STATUS", login_response.status_code, login_response.headers.get("Location"))

    # reset password
    request_client = Client()
    reset_request = request_client.post(reverse("password_reset_request"), {"email": email}, follow=False)
    print("RESET_REQ_STATUS", reset_request.status_code, reset_request.headers.get("Location"))
    print("EMAIL_BACKEND", settings.EMAIL_BACKEND)
    if settings.EMAIL_BACKEND.endswith("filebased.EmailBackend"):
        print("EMAIL_FILE_COUNT", len(list(Path(settings.EMAIL_FILE_PATH).glob("*"))))

    reset_code = PasswordResetCode.objects.filter(email=email).order_by("-created_at").first()
    print("RESET_CODE_CREATED", bool(reset_code))
    if reset_code:
        confirm_response = request_client.post(
            reverse("password_reset_confirm"),
            {
                "code": reset_code.code,
                "new_password1": new_password,
                "new_password2": new_password,
            },
            follow=False,
        )
        print("RESET_CONFIRM_STATUS", confirm_response.status_code, confirm_response.headers.get("Location"))

    login_new_client = Client()
    login_new_response = login_new_client.post(
        reverse("account_login"),
        {"login": username, "password": new_password},
        follow=False,
    )
    print("LOGIN_NEW_PASSWORD", login_new_response.status_code, login_new_response.headers.get("Location"))

    category = Category.objects.create(name=f"Smoke Category {suffix}")
    product = Product.objects.create(
        category=category,
        name=f"Smoke Product {suffix}",
        brand="SmokeBrand",
        sku=f"SMOKE-{suffix}",
        description="Smoke test product",
        price="1000.00",
        stock_qty=2,
        is_active=True,
    )
    variant = ProductVariant.objects.create(product=product, name="Blue", stock_qty=1)
    zero_product = Product.objects.create(
        category=category,
        name=f"Zero Product {suffix}",
        brand="SmokeBrand",
        sku=f"ZERO-{suffix}",
        description="Out of stock",
        price="500.00",
        stock_qty=0,
        is_active=True,
    )

    detail_response = login_new_client.get(reverse("product_detail", args=[product.slug]))
    print("DETAIL_STATUS", detail_response.status_code)

    no_variant_response = login_new_client.post(reverse("add_to_cart", args=[product.id]), {}, follow=False)
    print("ADD_NO_VARIANT_STATUS", no_variant_response.status_code, no_variant_response.json())

    zero_response = login_new_client.post(reverse("add_to_cart", args=[zero_product.id]), {}, follow=False)
    print("ADD_ZERO_STOCK_STATUS", zero_response.status_code, zero_response.json())

    add_response = login_new_client.post(reverse("add_to_cart", args=[product.id]), {"variant_id": variant.id}, follow=False)
    print("ADD_VARIANT_STATUS", add_response.status_code, add_response.json())

    overflow_response = login_new_client.post(reverse("add_to_cart", args=[product.id]), {"variant_id": variant.id}, follow=False)
    print("ADD_OVERFLOW_STATUS", overflow_response.status_code, overflow_response.json())

    cart_key = f"{product.id}:{variant.id}"
    cart_update_response = login_new_client.post(reverse("cart_update"), {"cart_key": cart_key, "quantity": "1"}, follow=False)
    print("CART_UPDATE_STATUS", cart_update_response.status_code, cart_update_response.headers.get("Location"))

    original_send = views.send_telegram_message

    def fake_send(text):
        sent_payload["text"] = text
        return {"ok": True}

    order_count_before = Order.objects.count()

    views.send_telegram_message = fake_send
    try:
        checkout_response = login_new_client.get(reverse("checkout"))
        print("CHECKOUT_STATUS", checkout_response.status_code)

        place_response = login_new_client.post(reverse("place_order"), {}, follow=False)
        print("PLACE_STATUS", place_response.status_code)
    finally:
        views.send_telegram_message = original_send

    order = Order.objects.order_by("-id").first()
    if order and Order.objects.count() <= order_count_before:
        order = None
    order_item = order.items.first() if order else None
    variant.refresh_from_db()
    print("ORDER_CREATED", bool(order))
    print("ORDER_VARIANT", order_item.variant_name if order_item else None)
    print("STOCK_AFTER_ORDER", variant.stock_qty)
    print("TG_HAS_VARIANT", "Варіант: Blue" in sent_payload.get("text", ""))
    print("ORDER_ADMIN", Order in admin.site._registry)
    print("REVIEW_ADMIN", Review in admin.site._registry)

    review_response = login_new_client.post(
        reverse("add_product_review", args=[product.slug]),
        {"product-rating": "5", "product-text": "Тестовий відгук"},
        follow=False,
    )
    print("REVIEW_STATUS", review_response.status_code, review_response.headers.get("Location"))
    review = Review.objects.filter(user=user, product=product).first()
    print("REVIEW_APPROVED", review.is_approved if review else None)

    add_again_response = login_new_client.post(reverse("add_to_cart", args=[product.id]), {"variant_id": variant.id}, follow=False)
    print("ADD_AFTER_DEPLETION_STATUS", add_again_response.status_code, add_again_response.json())


if __name__ == "__main__":
    main()
