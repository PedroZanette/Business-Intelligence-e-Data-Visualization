import scrapy


class GiassiSpider(scrapy.Spider):
    name = "giassi_arroz"
    start_urls = [
        "https://www.giassi.com.br/sitemap.xml",
    ]

    def start_requests(self):
        open("arroz_giassi.txt", "w", encoding="utf-8").close()
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urls = response.xpath('//*[local-name()="loc"]/text()').getall()

        for url in urls:
            if "product-" in url:
                yield response.follow(url, callback=self.parse_products)

    def parse_products(self, response):
        produtos = response.xpath('//*[local-name()="loc"]/text()').getall()

        for url in produtos:
            url_lower = url.lower()

            slug = url_lower.split("/")[-2]

            if slug.startswith("arroz"):
                print("ARROZ ENCONTRADO:", slug)
                yield response.follow(url, callback=self.parse_details)

    def parse_details(self, response):
        nome = response.xpath('//meta[@property="og:title"]/@content').get()
        marca = response.xpath('//meta[contains(@property,"product:brand")]/@content').get()
        preco = response.xpath('//meta[contains(@property,"product:price:amount")]/@content').get()
        categoria = response.xpath('//meta[contains(@property,"product:category")]/@content').get()

        if nome:
            nome = nome.strip()

        if marca:
            marca = marca.strip()

        if preco:
            preco = preco.strip()
            preco = f"R$ {preco.replace('.', ',')}"

        if categoria:
            categoria = categoria.strip()
            
        print("URL:", response.url)
        print("NOME:", nome)
        print("MARCA:", marca)
        print("PRECO:", preco)
        print("CATEGORIA:", categoria)
        print("-" * 50)

        if categoria and "arroz" in categoria.lower():
            with open("arroz_giassi.txt", "a", encoding="utf-8") as arquivo:
                arquivo.write(f"Nome: {nome}\n")
                arquivo.write(f"Marca: {marca}\n")
                arquivo.write(f"Preço: {preco}\n")
                arquivo.write(f"Categoria: {categoria}\n")
                arquivo.write(f"URL: {response.url}\n")
                arquivo.write("-" * 50 + "\n")

            yield {
                "nome": nome,
                "marca": marca,
                "preco": preco,
                "categoria": categoria,
                "url": response.url,
            }
