from bs4 import BeautifulSoup
import requests
import time

def get_html():
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        request_page = requests.get('https://spb.hh.ru/search/vacancy?L_is_autosearch=false&area=2&clusters=true&enable_snippets=true&text=Python&page=32', headers=headers)
        print('Getting HTML-code')
        return request_page.text

def get_offers_links():
        soup = BeautifulSoup(get_html(), 'lxml')
        offers_links = soup.find_all('a', class_='bloko-link HH-LinkModifier')
        print(offers_links)

get_offers_links()