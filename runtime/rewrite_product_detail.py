from pathlib import Path

product_detail = """{% load static %}
<!DOCTYPE html>
<html lang=\"uk\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <meta name=\"csrf-token\" content=\"{{ csrf_token }}\">
    <title>{{ product.name }} | VapeLand</title>
    <link rel=\"stylesheet\" href=\"{% static 'style.css' %}?v=20260414-3\">
</head>
<body>
    <div class=\"glow-bg\"></div>

    {% include 'includes/site_header.html' %}

    <section class=\"section container\">
        {% if messages %}
        <div class=\"messages-stack messages-stack--spaced\">
            {% for message in messages %}
            <div class=\"message-chip\">{{ message }}</div>
            {% endfor %}
        </div>
        {% endif %}

        <div class=\"order-layout order-layout--top\">
            <div class=\"auth-card auth-card--full\">
                <div class=\"card-image card-image--detail\">
                    {% if product.image %}
                    <img id=\"main-product-image\" src=\"{{ product.image.url }}\" alt=\"{{ product.name }}\" class=\"product-detail-image\">
                    {% else %}
                    <img id=\"main-product-image\" src=\"https://via.placeholder.com/700x520?text=VapeLand\" alt=\"{{ product.name }}\" class=\"product-detail-image\">
                    {% endif %}
                </div>
            </div>

            <div class=\"auth-card auth-card--full auth-card--left\">
                <p class=\"section-kicker section-kicker--compact\">{{ product.brand|default:\"VapeLand\"|upper }}</p>
                <h1 class=\"section-title section-title--compact\">{{ product.name }}</h1>
                <p class=\"section-copy section-copy--compact\">{{ product.description|default:\"\u041e\u0440\u0438\u0433\u0456\u043d\u0430\u043b\u044c\u043d\u0438\u0439 \u0442\u043e\u0432\u0430\u0440 VapeLand \u0437 \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u044e \u0446\u0456\u043d\u043e\u044e \u0442\u0430 \u0448\u0432\u0438\u0434\u043a\u043e\u044e \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u043e\u044e.\" }}</p>
                {% if product.discount_data.has_discount %}
                <div class=\"product-pricing-block\">
                    <span class=\"discount-badge discount-badge--inline\">{{ product.discount_data.discount_badge }}</span>
                    <div class=\"price-stack price-stack--detail\">
                        <span class=\"price-old\">{{ product.discount_data.base_price|floatformat:0 }} \u0433\u0440\u043d</span>
                        <span class=\"price-current\">{{ product.discount_data.final_price|floatformat:0 }} \u0433\u0440\u043d</span>
                    </div>
                    <p class=\"discount-caption discount-caption--detail\">{{ product.discount_data.discount_label }}</p>
                </div>
                {% else %}
                <div class=\"price-tag price-tag--inline\">{{ product.discount_data.final_price|floatformat:0 }} \u0433\u0440\u043d</div>
                {% endif %}
                {% if product.includes_glycerin %}
                <div class=\"included-addon\" aria-label=\"\u041e\u0431\u043e\u0432\u2019\u044f\u0437\u043a\u043e\u0432\u0430 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0430\u0446\u0456\u044f\">
                    <span class=\"included-addon__icon\">?</span>
                    <span>\u0412 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0456: \u0413\u043b\u0456\u0446\u0435\u0440\u0438\u043d (+{{ product.effective_glycerin_price|floatformat:0 }} \u0433\u0440\u043d)</span>
                </div>
                {% endif %}

                {% if variants %}
                <div class=\"variant-block\">
                    <strong class=\"variant-block-title\">\u041e\u0431\u0435\u0440\u0456\u0442\u044c \u0432\u0430\u0440\u0456\u0430\u043d\u0442</strong>
                    <div class=\"variant-block-list\">
                        {% for variant in variants %}
                        <button type=\"button\" class=\"btn-ghost product-variant-btn\" data-variant-id=\"{{ variant.id }}\" data-variant-name=\"{{ variant.name }}\" data-variant-stock=\"{{ variant.stock_qty|default_if_none:'' }}\" {% if variant.stock_qty == 0 or not variant.is_active %}disabled{% endif %}>
                            {{ variant.name }}{% if variant.stock_qty == 0 %} \u2022 \u043d\u0435\u043c\u0430\u0454{% endif %}
                        </button>
                        {% endfor %}
                    </div>
                </div>
                {% endif %}

                <div id=\"product-stock-note\" class=\"summary-note summary-note--spaced\">
                    {% if product.stock_qty == 0 %}\u041d\u0435\u043c\u0430\u0454 \u0432 \u043d\u0430\u044f\u0432\u043d\u043e\u0441\u0442\u0456.
                    {% elif product.stock_qty %}\u0423 \u043d\u0430\u044f\u0432\u043d\u043e\u0441\u0442\u0456: {{ product.stock_qty }} \u0448\u0442.
                    {% else %}\u041d\u0430\u044f\u0432\u043d\u0456\u0441\u0442\u044c \u0443\u0442\u043e\u0447\u043d\u044e\u0439\u0442\u0435 \u0443 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u0430.
                    {% endif %}
                </div>

                <div class=\"stack-actions\">
                    <button type=\"button\" id=\"add-to-cart-button\" class=\"btn-primary\" {% if variants or product.stock_qty == 0 and not variants %}disabled{% endif %}>
                        {% if variants %}\u041e\u0411\u0415\u0420\u0406\u0422\u042c \u0412\u0410\u0420\u0406\u0410\u041d\u0422{% elif product.stock_qty == 0 and not variants %}\u041d\u0415\u041c\u0410\u0404 \u0412 \u041d\u0410\u042f\u0412\u041d\u041e\u0421\u0422\u0406{% else %}\u0414\u041e\u0414\u0410\u0422\u0418 \u0423 \u041a\u041e\u0428\u0418\u041a{% endif %}
                    </button>
                    <a href=\"{% url 'catalog_page' %}\" class=\"btn-ghost btn-link-block\">\u041f\u043e\u0432\u0435\u0440\u043d\u0443\u0442\u0438\u0441\u044f \u0434\u043e \u043a\u0430\u0442\u0430\u043b\u043e\u0433\u0443</a>
                </div>
            </div>
        </div>
    </section>

    {% include 'includes/support_widget.html' %}

    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
            const addToCartButton = document.getElementById('add-to-cart-button');
            const stockNote = document.getElementById('product-stock-note');
            const variantButtons = document.querySelectorAll('.product-variant-btn');
            let selectedVariantId = null;

            const setStockState = (stockValue) => {
                if (stockValue === '' || stockValue === null || typeof stockValue === 'undefined') {
                    addToCartButton.disabled = false;
                    addToCartButton.textContent = 'ДОДАТИ У КОШИК';
                    return;
                }

                const parsed = Number(stockValue);
                if (!Number.isNaN(parsed) && parsed <= 0) {
                    addToCartButton.disabled = true;
                    addToCartButton.textContent = 'НЕМАЄ В НАЯВНОСТІ';
                    if (stockNote) stockNote.textContent = 'Немає в наявності.';
                } else {
                    addToCartButton.disabled = false;
                    addToCartButton.textContent = 'ДОДАТИ У КОШИК';
                    if (stockNote) stockNote.textContent = `У наявності: ${parsed} шт.`;
                }
            };

            variantButtons.forEach((button) => {
                button.addEventListener('click', () => {
                    variantButtons.forEach((item) => item.classList.remove('is-active'));
                    button.classList.add('is-active');
                    selectedVariantId = button.dataset.variantId;
                    setStockState(button.dataset.variantStock);
                });
            });

            addToCartButton?.addEventListener('click', () => {
                if (variantButtons.length && !selectedVariantId) {
                    window.alert('Оберіть варіант товару.');
                    return;
                }

                const body = new URLSearchParams();
                if (selectedVariantId) {
                    body.set('variant_id', selectedVariantId);
                }

                fetch(`/cart/add/{{ product.id }}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: body.toString(),
                })
                    .then(async (response) => {
                        const data = await response.json();
                        if (!response.ok) {
                            throw new Error(data.message || 'Не вдалося додати товар у кошик.');
                        }
                        return data;
                    })
                    .then((data) => {
                        const cartCount = document.getElementById('cart-count');
                        if (cartCount) {
                            cartCount.innerText = data.cart_count;
                        }
                        location.reload();
                    })
                    .catch((error) => {
                        window.alert(error.message);
                    });
            });
        });
    </script>
</body>
</html>
"""

Path(r"D:/Python/Deepsmoke/app/app_web/templates/product_detail.html").write_text(product_detail, encoding="utf-8")
