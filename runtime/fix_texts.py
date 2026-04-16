from pathlib import Path


def apply_replacements(path, replacements):
    text = Path(path).read_text(encoding='utf-8')
    for old, new in replacements:
        text = text.replace(old, new)
    Path(path).write_text(text, encoding='utf-8')

catalog_replacements = [
    ('    <title>??????? | VapeLand</title>', '    <title>\u041a\u0430\u0442\u0430\u043b\u043e\u0433 | VapeLand</title>'),
    ('            <h2 class="modal-title">???? ? <span>VapeLand</span></h2>', '            <h2 class="modal-title">\u0412\u0445\u0456\u0434 \u0443 <span>VapeLand</span></h2>'),
    ('            <p class="modal-subtitle">???????? ? ???? ??????, ??? ??????????? ?????????? ?????? ?? ?????? ??????? ???????.</p>', '            <p class="modal-subtitle">\u0423\u0432\u0456\u0439\u0434\u0456\u0442\u044c \u0443 \u0441\u0432\u0456\u0439 \u0430\u043a\u0430\u0443\u043d\u0442, \u0449\u043e\u0431 \u043e\u0444\u043e\u0440\u043c\u043b\u044e\u0432\u0430\u0442\u0438 \u0437\u0430\u043c\u043e\u0432\u043b\u0435\u043d\u043d\u044f \u0448\u0432\u0438\u0434\u0448\u0435 \u0442\u0430 \u0431\u0430\u0447\u0438\u0442\u0438 \u0456\u0441\u0442\u043e\u0440\u0456\u044e \u043f\u043e\u043a\u0443\u043f\u043e\u043a.</p>'),
    ('                ?????? ????? Google', '                \u0423\u0432\u0456\u0439\u0442\u0438 \u0447\u0435\u0440\u0435\u0437 Google'),
    ('                    <h2>??????? ???????</h2>', '                    <h2>\u041a\u0430\u0442\u0430\u043b\u043e\u0433 \u0442\u043e\u0432\u0430\u0440\u0456\u0432</h2>'),
    ('                        ??? ??????', '                        \u0423\u0441\u0456 \u0442\u043e\u0432\u0430\u0440\u0438'),
    ('                        <p class="section-kicker">???????</p>', '                        <p class="section-kicker">\u041a\u0430\u0442\u0430\u043b\u043e\u0433</p>'),
    ('                                ??? <span>??????</span>', '                                \u0423\u0441\u0456 <span>\u0442\u043e\u0432\u0430\u0440\u0438</span>'),
    ('                            ?????????? ?????? ?? ??????? "{{ search_query }}".', '                            \u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u043f\u043e\u0448\u0443\u043a\u0443 \u0437\u0430 \u0437\u0430\u043f\u0438\u0442\u043e\u043c "{{ search_query }}".'),
    ('                            ???????? ????????? ??????? VapeLand ?? ????????? ?? ? ????? ??? ?????? ??????.', '                            \u041e\u0431\u0438\u0440\u0430\u0439\u0442\u0435 \u0430\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0456 \u043f\u043e\u0437\u0438\u0446\u0456\u0457 VapeLand \u0442\u0430 \u0434\u043e\u0434\u0430\u0432\u0430\u0439\u0442\u0435 \u0457\u0445 \u0443 \u043a\u043e\u0448\u0438\u043a \u0431\u0435\u0437 \u0437\u0430\u0439\u0432\u0438\u0445 \u043a\u0440\u043e\u043a\u0456\u0432.'),
    ('                    <div class="catalog-filter-note">{{ products_total }} ???????</div>', '                    <div class="catalog-filter-note">{{ products_total }} \u0442\u043e\u0432\u0430\u0440\u0456\u0432</div>'),
    (' ???</span>', ' \u0433\u0440\u043d</span>'),
    ('                                <p class="review-empty review-empty--spaced">????? ? ?????????</p>', '                                <p class="review-empty review-empty--spaced">\u041d\u0435\u043c\u0430\u0454 \u0432 \u043d\u0430\u044f\u0432\u043d\u043e\u0441\u0442\u0456</p>'),
    ('                                ????? ? ?????????', '                                \u041d\u0415\u041c\u0410\u0404 \u0412 \u041d\u0410\u042f\u0412\u041d\u041e\u0421\u0422\u0406'),
    ('                                ?????? ???????', '                                \u041e\u0411\u0420\u0410\u0422\u0418 \u0412\u0410\u0420\u0406\u0410\u041d\u0422'),
    ('                                ? ?????', '                                \u0423 \u041a\u041e\u0428\u0418\u041a'),
    ('                        <h3 class="flush-title">??????? ?? ????????</h3>', '                        <h3 class="flush-title">\u0422\u043e\u0432\u0430\u0440\u0456\u0432 \u043d\u0435 \u0437\u043d\u0430\u0439\u0434\u0435\u043d\u043e</h3>'),
    ('                        <p class="review-empty">????????? ??????? ????????? ????? ??? ??????? ???? ?????????.</p>', '                        <p class="review-empty">\u0421\u043f\u0440\u043e\u0431\u0443\u0439\u0442\u0435 \u0437\u043c\u0456\u043d\u0438\u0442\u0438 \u043f\u043e\u0448\u0443\u043a\u043e\u0432\u0438\u0439 \u0437\u0430\u043f\u0438\u0442 \u0430\u0431\u043e \u0432\u0438\u0431\u0440\u0430\u0442\u0438 \u0456\u043d\u0448\u0443 \u043a\u0430\u0442\u0435\u0433\u043e\u0440\u0456\u044e.</p>'),
    ('class="btn-ghost">?????</a>', 'class="btn-ghost">\u041d\u0430\u0437\u0430\u0434</a>'),
    ('                    <span class="catalog-pagination__status">???????? {{ page_obj.number }} ? {{ page_obj.paginator.num_pages }}</span>', '                    <span class="catalog-pagination__status">\u0421\u0442\u043e\u0440\u0456\u043d\u043a\u0430 {{ page_obj.number }} \u0437 {{ page_obj.paginator.num_pages }}</span>'),
    ('class="btn-ghost">????</a>', 'class="btn-ghost">\u0414\u0430\u043b\u0456</a>'),
    ("throw new Error(data.message || '?? ??????? ?????? ????? ? ?????.');", "throw new Error(data.message || '\u041d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0434\u043e\u0434\u0430\u0442\u0438 \u0442\u043e\u0432\u0430\u0440 \u0443 \u043a\u043e\u0448\u0438\u043a.');"),
]

apply_replacements(r'D:/Python/Deepsmoke/app/app_web/templates/catalog.html', catalog_replacements)
