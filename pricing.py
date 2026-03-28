from decimal import Decimal, ROUND_HALF_UP

from .models import Product


DISCOUNT_RATE_3_THRESHOLD = Decimal('550.00')
DISCOUNT_RATE_5_THRESHOLD = Decimal('1050.00')
DISCOUNT_RATE_3 = Decimal('0.03')
DISCOUNT_RATE_5 = Decimal('0.05')
BIRTHDAY_BONUS = Decimal('150.00')


def money(value):
    if not isinstance(value, Decimal):
        value = Decimal(str(value))
    return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def normalize_city(city):
    value = (city or '').strip().lower()
    replacements = ('м.', 'м ', '.', ',')
    for item in replacements:
        value = value.replace(item, ' ')
    return ' '.join(value.split())


def is_mykolaiv(city):
    normalized = normalize_city(city)
    return any(name in normalized for name in ('миколаїв', 'миколаев', 'mykolaiv', 'nikolaev'))


def get_cart_items(cart):
    cart_items = []

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id), is_active=True)
        except (Product.DoesNotExist, TypeError, ValueError):
            continue

        item_total = money(product.price * quantity)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })

    return cart_items


def calculate_cart_summary(cart_items, city='', birthday_bonus_selected=False):
    subtotal = money(sum((item['total'] for item in cart_items), Decimal('0.00')))

    if subtotal >= DISCOUNT_RATE_5_THRESHOLD:
        percent_rate = DISCOUNT_RATE_5
        percent_label = 'Знижка 5% на чек'
    elif subtotal >= DISCOUNT_RATE_3_THRESHOLD:
        percent_rate = DISCOUNT_RATE_3
        percent_label = 'Знижка 3% на чек'
    else:
        percent_rate = Decimal('0.00')
        percent_label = 'Знижка за сумою не застосовується'

    percent_discount = money(subtotal * percent_rate)
    birthday_discount = Decimal('0.00')
    if birthday_bonus_selected:
        available_after_percent = max(Decimal('0.00'), subtotal - percent_discount)
        birthday_discount = money(min(BIRTHDAY_BONUS, available_after_percent))

    total_discount = money(percent_discount + birthday_discount)
    final_total = money(max(Decimal('0.00'), subtotal - total_discount))

    city_is_mykolaiv = is_mykolaiv(city)
    delivery_is_free = city_is_mykolaiv or subtotal >= DISCOUNT_RATE_5_THRESHOLD
    if city_is_mykolaiv:
        delivery_label = 'Безкоштовна доставка по м.Миколаїв'
    elif subtotal >= DISCOUNT_RATE_5_THRESHOLD:
        delivery_label = 'Безкоштовна доставка по Україні'
    else:
        delivery_label = 'Доставка за тарифами перевізника'

    return {
        'subtotal': subtotal,
        'percent_rate': percent_rate,
        'percent_discount': percent_discount,
        'percent_label': percent_label,
        'birthday_discount': birthday_discount,
        'birthday_bonus_selected': birthday_bonus_selected,
        'birthday_verification_required': birthday_bonus_selected,
        'total_discount': total_discount,
        'final_total': final_total,
        'delivery_is_free': delivery_is_free,
        'delivery_label': delivery_label,
        'city_is_mykolaiv': city_is_mykolaiv,
    }
