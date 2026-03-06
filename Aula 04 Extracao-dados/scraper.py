import requests
import traceback
import time
import random

from dataclasses import dataclass

from bs4 import BeautifulSoup, element

@dataclass
class Noticia():
    link: str
    titulo: str
    tema: str
    chamada: str
    url_imagem: str
    data: str
    texto: str

def print_log_and_exit(message:str, log: str):
    print(message)
    open("Error_log.txt",'w').write(log)
    exit(1)

def conect_and_parse(url)->BeautifulSoup | None:
    print(f"Tentando conexão em {url}")
    #Headers HTTP. O User-Agent usado "informa" que a conexão é feita por um browser
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"} 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("\tConexão bem sucedida.")
        return BeautifulSoup(response.text)
    print(f"\tERRO buscando página: {response.status_code}-{response.text}")
    return None

def get_text(elemento: element.Tag | None):
    if elemento is not None:
        return elemento.get_text(strip=True)
    return ''

def get_attribute(elemento: element.Tag | None, atributo: str):
    if elemento is not None and elemento.has_attr(atributo):
        return elemento.get(atributo)
    return ''

def download_image(img_url: str, path_prefix: str):
    index_barra = img_url.rfind('/')
    if(index_barra != -1):
        nome_imagem = img_url[index_barra+1:]
    else:
        nome_imagem = 'img_desconhecida'
    response = requests.get(img_url)
    if response.status_code==200:
        with open(f"{path_prefix}/{nome_imagem}",'wb') as f:
            f.write(response.content)



def parse_noticia_destaque(elemento: element.Tag) -> Noticia:
    #extrair Imagem, Título e Link da Notícia
    link = get_attribute(elemento.find_next('a'), 'href')
    img_url = get_attribute(elemento.find_next('img'),'src')
    tema = get_text(elemento.find_next('div',{'class':'news-hat-3'}))
    titulo = get_text(elemento.find_next('div',{'class':'news-hat-3'}))
    data = ''
    return Noticia(str(link), titulo, tema, '', str(img_url), data, texto='')

def parse_noticia_arquivo(elemento: element.Tag) -> Noticia:
    #extrair Imagem, Título e Link da Notícia
    link = get_attribute(elemento.find_next('a'), 'href')
    img_url = get_attribute(elemento.find_next('img'),'src')
    tema = get_text(elemento.find_next('div',{'class':'news-hat-3'}))
    titulo = get_text(elemento.find_next('h3'))
    data = get_text(elemento.find_next('span',{'class':'text-indata'}))
    return Noticia(str(link), titulo, tema, '', str(img_url), data, texto='')

def processa_pagina_noticia(url_base, noticia: Noticia):
    if not noticia.link.startswith(url_base):
        print("Tentando processar link de outra página!\n\t{noticia.link}")
        return
    
    tree = conect_and_parse(noticia.link)

    print(f"Extraindo conteúdo da notícia {noticia.titulo}")
    if tree is None:
        print("ERRO processando arquivo da notícia")
        return

    container_titulo = tree.find('div',{'class':'page-title-large'})
    if container_titulo is not None:
        noticia.titulo = get_text(container_titulo.find_next('h1', {'id':'main-title'}))
        noticia.chamada = get_text(container_titulo.find_next('div',{'id':'sub-title'}))
        noticia.data = str(get_attribute(container_titulo.find_next('time'),'datetime'))

    container_media = tree.find('section', {'class':'featured-media'})
    if container_media is not None:
        noticia.url_imagem = str(get_attribute(container_media.find_next('img'),'src'))
        download_image(noticia.url_imagem, "imagens")

    artigo = tree.find('div', {'itemprop':'articleBody'})
    if artigo is not None:
        noticia.texto = artigo.get_text()


    return

url_base = "https://iclnoticias.com.br"
response = requests.get(f"{url_base}/politica")

try:
        tree = conect_and_parse(f"{url_base}/politica")
        if tree is None:
            print_log_and_exit("Falha no parse HTML", response.text)
        #Container principal notícia: <div class="news-wrap">
        els_noticias_destaque = tree.find_all('div',{'class':'news-wrap'})
        els_noticias_arquivo = tree.find_all('div', {'class':'c-archive'})

        noticias = [parse_noticia_destaque(n) for n in els_noticias_destaque]
        noticias.extend([parse_noticia_arquivo(n) for n in els_noticias_arquivo])

        for noticia in  noticias:
            processa_pagina_noticia(url_base, noticia)
            #Delay de alguns segundos entre cada conexão
            delay = round(random.uniform(2.0, 5.0),2)
            time.sleep(delay) 

        print(f"Número de notícias recuperadas:{len(noticias)}")
        with open('Noticias_extraidas.txt','w',encoding='utf-8') as extracao:
            for noticia in noticias:
                print(f"{noticia.titulo}\n\t{noticia.data}\n\n")
                substr_len = len(noticia.texto) if len(noticia.texto) > 50 else 50 
                print(f"{noticia.texto[0:substr_len]}")
                extracao.write(f"{noticia.titulo}\n\t{noticia.data}\n\n{noticia.texto[0:substr_len]}")
                extracao.write("\t\t----------------\t\t\n\n")

except Exception as e:
    log = traceback.format_exc()
    print_log_and_exit(f"-!-!-!-!-!-!\nException não tratada:\n\n{log}", log)