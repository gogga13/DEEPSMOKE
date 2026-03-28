from .pricing import calculate_cart_summary, get_cart_items

def cart_processor(request):
    cart = request.session.get('cart', {})
    cart_items = get_cart_items(cart)
    city = ''
    if getattr(request, 'user', None) and request.user.is_authenticated and hasattr(request.user, 'profile'):
        city = request.user.profile.city or ''

    cart_summary = calculate_cart_summary(cart_items, city=city, birthday_bonus_selected=False)

    return {
        'cart_count': sum(cart.values()) if cart else 0,
        'cart_total': cart_summary['subtotal'],
        'cart_products': cart_items,
        'cart_summary': cart_summary,
    }
