from pathlib import Path

def apply(path, reps):
    t = Path(path).read_text(encoding='utf-8')
    for a,b in reps:
        t = t.replace(a,b)
    Path(path).write_text(t, encoding='utf-8')

reps = [
('                    {{ product.description|default:"???????????? ????? VapeLand ? ?????????? ????? ?? ??????? ?????????." }}','                    {{ product.description|default:"\u041e\u0440\u0438\u0433\u0456\u043d\u0430\u043b\u044c\u043d\u0438\u0439 \u0442\u043e\u0432\u0430\u0440 VapeLand \u0437 \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u043e\u044e \u0446\u0456\u043d\u043e\u044e \u0442\u0430 \u0448\u0432\u0438\u0434\u043a\u043e\u044e \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u043e\u044e." }}'),
(' ???</span>', ' \u0433\u0440\u043d</span>'),
('                <div class="included-addon" aria-label="????\'?????? ????????????">','                <div class="included-addon" aria-label="\u041e\u0431\u043e\u0432\'\u044f\u0437\u043a\u043e\u0432\u0430 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0430\u0446\u0456\u044f">'),
('                    <span>? ?????????: ???????? (+{{ product.effective_glycerin_price|floatformat:0 }} ???)</span>','                    <span>\u0412 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0456: \u0413\u043b\u0456\u0446\u0435\u0440\u0438\u043d (+{{ product.effective_glycerin_price|floatformat:0 }} \u0433\u0440\u043d)</span>'),
('                    <strong class="variant-block-title">??????? ???????</strong>','                    <strong class="variant-block-title">\u041e\u0431\u0435\u0440\u0456\u0442\u044c \u0432\u0430\u0440\u0456\u0430\u043d\u0442</strong>'),
('{% if variant.stock_qty == 0 %} ? ?????{% endif %}','{% if variant.stock_qty == 0 %} \u2022 \u043d\u0435\u043c\u0430\u0454{% endif %}'),
('                    ????? ? ?????????.','                    \u041d\u0435\u043c\u0430\u0454 \u0432 \u043d\u0430\u044f\u0432\u043d\u043e\u0441\u0442\u0456.'),
('                    ? ?????????: {{ product.stock_qty }} ??.','                    \u0423 \u043d\u0430\u044f\u0432\u043d\u043e\u0441\u0442\u0456: {{ product.stock_qty }} \u0448\u0442.'),
('                    ????????? ????????? ? ?????????.','                    \u041d\u0430\u044f\u0432\u043d\u0456\u0441\u0442\u044c \u0443\u0442\u043e\u0447\u043d\u044e\u0439\u0442\u0435 \u0443 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u0430.'),
('{% if variants %}??????? ???????{% elif product.stock_qty == 0 and not variants %}????? ? ?????????{% else %}?????? ? ?????{% endif %}','{% if variants %}\u041e\u0411\u0415\u0420\u0406\u0422\u042c \u0412\u0410\u0420\u0406\u0410\u041d\u0422{% elif product.stock_qty == 0 and not variants %}\u041d\u0415\u041c\u0410\u0404 \u0412 \u041d\u0410\u042f\u0412\u041d\u041e\u0421\u0422\u0406{% else %}\u0414\u041e\u0414\u0410\u0422\u0418 \u0423 \u041a\u041e\u0428\u0418\u041a{% endif %}'),
('                    <a href="{% url \'catalog_page\' %}" class="btn-ghost btn-link-block">??????????? ?? ????????</a>','                    <a href="{% url \'catalog_page\' %}" class="btn-ghost btn-link-block">\u041f\u043e\u0432\u0435\u0440\u043d\u0443\u0442\u0438\u0441\u044f \u0434\u043e \u043a\u0430\u0442\u0430\u043b\u043e\u0433\u0443</a>'),
('                    <p class="section-kicker">???????</p>','                    <p class="section-kicker">\u0412\u0456\u0434\u0433\u0443\u043a\u0438</p>'),
('                    <h2 class="section-title">??????? <span>??? ?????</span></h2>','                    <h2 class="section-title">\u0412\u0456\u0434\u0433\u0443\u043a\u0438 <span>\u043f\u0440\u043e \u0442\u043e\u0432\u0430\u0440</span></h2>'),
('                    <p class="section-copy">??????? ??????: {{ review_average|floatformat:1 }} / 5 ? {{ review_count }} ????????</p>','                    <p class="section-copy">\u0421\u0435\u0440\u0435\u0434\u043d\u044f \u043e\u0446\u0456\u043d\u043a\u0430: {{ review_average|floatformat:1 }} / 5 \u2022 {{ review_count }} \u0432\u0456\u0434\u0433\u0443\u043a\u0456\u0432</p>'),
('                <p class="review-empty">???? ?? ????? ????????? ???????? ?? ????? ??????.</p>','                <p class="review-empty">\u041f\u043e\u043a\u0438 \u0449\u043e \u043d\u0435\u043c\u0430\u0454 \u0441\u0445\u0432\u0430\u043b\u0435\u043d\u0438\u0445 \u0432\u0456\u0434\u0433\u0443\u043a\u0456\u0432 \u043f\u043e \u0446\u044c\u043e\u043c\u0443 \u0442\u043e\u0432\u0430\u0440\u0443.</p>'),
('                <h3 class="flush-title">???????? ??????</h3>','                <h3 class="flush-title">\u0417\u0430\u043b\u0438\u0448\u0438\u0442\u0438 \u0432\u0456\u0434\u0433\u0443\u043a</h3>'),
('                    <button type="submit" class="btn-primary btn-block">????????? ??????</button>','                    <button type="submit" class="btn-primary btn-block">\u041d\u0430\u0434\u0456\u0441\u043b\u0430\u0442\u0438 \u0432\u0456\u0434\u0433\u0443\u043a</button>'),
('                <p class="review-empty">??? ???????? ??????, ???????? ? ???? ??????.</p>','                <p class="review-empty">\u0429\u043e\u0431 \u0437\u0430\u043b\u0438\u0448\u0438\u0442\u0438 \u0432\u0456\u0434\u0433\u0443\u043a, \u0443\u0432\u0456\u0439\u0434\u0456\u0442\u044c \u0443 \u0441\u0432\u0456\u0439 \u0430\u043a\u0430\u0443\u043d\u0442.</p>'),
('                <a href="{% url \'account_login\' %}" class="btn-ghost btn-link-block">??????</a>','                <a href="{% url \'account_login\' %}" class="btn-ghost btn-link-block">\u0423\u0432\u0456\u0439\u0442\u0438</a>'),
('            <p class="section-kicker">????????????</p>','            <p class="section-kicker">\u0420\u0435\u043a\u043e\u043c\u0435\u043d\u0434\u0430\u0446\u0456\u0457</p>'),
('            <h2 class="section-title">????? <span>??????</span></h2>','            <h2 class="section-title">\u0421\u0445\u043e\u0436\u0456 <span>\u0442\u043e\u0432\u0430\u0440\u0438</span></h2>'),
('            <p class="section-kicker">??????????</p>','            <p class="section-kicker">\u0421\u0443\u043c\u0456\u0441\u043d\u0456\u0441\u0442\u044c</p>'),
('            <h2 class="section-title">??????? <span>???????</span></h2>','            <h2 class="section-title">\u0421\u0443\u043c\u0456\u0441\u043d\u0456 <span>\u043f\u043e\u0437\u0438\u0446\u0456\u0457</span></h2>'),
("addToCartButton.textContent = '?????? ? ?????';", "addToCartButton.textContent = '\u0414\u041e\u0414\u0410\u0422\u0418 \u0423 \u041a\u041e\u0428\u0418\u041a';"),
("addToCartButton.textContent = '????? ? ?????????';", "addToCartButton.textContent = '\u041d\u0415\u041c\u0410\u0404 \u0412 \u041d\u0410\u042f\u0412\u041d\u041e\u0421\u0422\u0406';"),
("if (stockNote) stockNote.textContent = '????? ? ?????????.';", "if (stockNote) stockNote.textContent = '\u041d\u0435\u043c\u0430\u0454 \u0432 \u043d\u0430\u044f\u0432\u043d\u043e\u0441\u0442\u0456.';"),
("if (stockNote) stockNote.textContent = `? ?????????: ${parsed} ??.`;", "if (stockNote) stockNote.textContent = `\u0423 \u043d\u0430\u044f\u0432\u043d\u043e\u0441\u0442\u0456: ${parsed} \u0448\u0442.`;"),
("window.alert('??????? ??????? ??????.');", "window.alert('\u041e\u0431\u0435\u0440\u0456\u0442\u044c \u0432\u0430\u0440\u0456\u0430\u043d\u0442 \u0442\u043e\u0432\u0430\u0440\u0443.');"),
("throw new Error(data.message || '?? ??????? ?????? ????? ? ?????.');", "throw new Error(data.message || '\u041d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0434\u043e\u0434\u0430\u0442\u0438 \u0442\u043e\u0432\u0430\u0440 \u0443 \u043a\u043e\u0448\u0438\u043a.');"),
]

apply(r'D:/Python/Deepsmoke/app/app_web/templates/product_detail.html', reps)
