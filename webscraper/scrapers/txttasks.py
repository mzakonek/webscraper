import requests
from bs4 import BeautifulSoup
import re


def scrap_text(link):
    res = requests.get(link)
    html_page = res.content

    soup = BeautifulSoup(html_page, "html.parser")
    data = soup.find_all(text=True)

    def visible(element):
        """extract from the page only the text and skip elements e.g. style, script..."""
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title', 'div', 'input', 'meta', 'noscript', 'header']:
            return False
        elif re.match('<!--.*-->', str(element.encode('utf-8'))):
            return False
        return True

    result = filter(visible, data)
    clean_text = []
    for i in result:
        if i.strip() != "":
            clean_text.append(i.strip())

    return clean_text


def save_scrapped_text(data, fileid, now=None):
    if now:
        now_as_txt = now.strftime("%d-%m-%y %H:%M:%S")
        filename = f'{fileid}_{now_as_txt}.txt'
    else:
        filename = f'{fileid}.txt'
    with open(f'scrapers/text_from_urls/{filename}', 'w+') as txtfile:
        for row in data:
            txtfile.write(row + '\n')

    return filename


def read_txt_file(filename):
    with open(f'scrapers/text_from_urls/{filename}', 'r') as text:
        data = text.read().splitlines()
    return data

