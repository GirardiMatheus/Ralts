import scrapy
from urllib.parse import urljoin

class ProductSpider(scrapy.Spider):
    name = "product_spider"
    allowed_domains = ["mercadolivre.com.br", "mercadolivre.com"]
    # exemplo de busca por "celular" — ajuste a query conforme necessário
    start_urls = [
        "https://lista.mercadolivre.com.br/celular"
    ]

    def parse(self, response):
        # itera sobre possíveis containers de produto (vários seletores para compatibilidade)
        product_selectors = response.css("li.ui-search-layout__item, .ui-search-result, .results-item, div.results-item")
        for product in product_selectors:
            # título — tenta múltiplos seletores comuns
            title = product.css(
                ".ui-search-item__title::text, .ui-search-result__title::text, h2::text, a.item__info-title::text"
            ).get()
            if title:
                title = title.strip()

            # preço — compõe parte inteira e centavos 
            price_int = product.css(
                ".price-tag-fraction::text, .andes-money-amount__fraction::text, .ui-search-price__part--price::text"
            ).get()
            price_dec = product.css(
                ".price-tag-cents::text, .andes-money-amount__cents::text"
            ).get()
            price = None
            if price_int:
                # normalize numeric parts (remove thousands separators)
                int_part = price_int.replace(".", "").replace(",", ".")
                if price_dec:
                    try:
                        price = float(f"{int_part}.{price_dec}")
                    except ValueError:
                        # fallback: try replacing comma
                        try:
                            price = float(int_part)
                        except Exception:
                            price = None
                else:
                    try:
                        price = float(int_part)
                    except Exception:
                        price = None

            # link relativo/absoluto
            link = product.css("a.ui-search-link::attr(href), a::attr(href)").get()
            if link:
                link = urljoin(response.url, link)

            # yield item (dicionário simples)
            if title or price or link:
                yield {
                    "title": title,
                    "price": price,
                    "link": link,
                    "source": "mercadolivre",
                }

        # seguir paginação (tenta seletores comuns para "próxima página")
        next_page = (
            response.css("a.andes-pagination__link--next::attr(href)").get()
            or response.css("a.ui-search-link[title='Próxima página']::attr(href)").get()
            or response.css("a.next::attr(href)").get()
        )
        if next_page:
            next_page = urljoin(response.url, next_page)
            yield scrapy.Request(next_page, callback=self.parse)
