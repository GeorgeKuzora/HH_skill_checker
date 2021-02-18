from bs4 import BeautifulSoup
import requests
import time

# Класс служит для того чтобы получить входные данные от пользователя
class User_input:
    def __init__(self):
        self.area = None
        self.query = None

    def get_input(self):
        self.area = input('Please enter an area code: ')
        self.query = input('Please enter a search query: ')
        return self.area, self.query

# Класс служит для того чтобы получить ссылки на сраницы с вакансиями.
class Get_href:

    def __init__(self, area, query):
        self.area = area
        self.query = query
        self.all_links = []

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        request_page = requests.get(url, headers = headers)
        print('Getting HTML-code from... %s' % url)
        return request_page.text

    def is_empty(self, html):
        soup = BeautifulSoup(html, 'lxml')
        _job_cards = soup.find_all('a', class_='bloko-link HH-LinkModifier') #'div', class_='vacancy-serp-item ')
        if not _job_cards:
            return True
        else:
            return False

    def get_offers_links(self, html):
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('a', class_='bloko-link HH-LinkModifier')
        for link in links:
            _offered_link = link.get('href').split('?')
            self.all_links.append(_offered_link[0])
        return self.all_links


    def get_all_links(self):
        _url_base = ['https://spb.hh.ru/search/vacancy?L_is_autosearch=false', '&clusters=true&enable_snippets=true']
        _url_area = '&area=' + str(self.area)
        _url_text = '&text=' + self.query
        _url_page = '&page='
        _page = 0

        page_is_not_empty = True

        while page_is_not_empty:
            url = str(_url_base[0] + _url_area + _url_base[1] + _url_text + _url_page + str(_page))
#            time.sleep(.1)
            html = self.get_html(url)
            if not self.is_empty(html):
                self.all_links = self.get_offers_links(html)
                _page += 1
            else:
                page_is_not_empty = False
        return self.all_links

class Get_required_skills:

    def __init__(self, job_offers):
        self.job_offers = job_offers
        self.skills = []
        self.description = []

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        request_page = requests.get(url, headers = headers)
        return request_page.text

    def get_skills(self):
        for link in self.job_offers:
            print('%d from %d' % (self.job_offers.index(link), len(self.job_offers)))
            html = self.get_html(link)
            soup = BeautifulSoup(html, 'lxml')
            skill_block = soup.find_all('span', class_='bloko-tag__section bloko-tag__section_text')
            for skill in skill_block:
                self.skills.append(skill.text)
        return self.skills

class Skills_count:
    
    def __init__(self, skills):
        self.skills = skills
        self.skills_set = set(skills)
        self.skills_dict = {}

    def skills_count(self):
        for uniq_skill in self.skills_set:
            self.skills_dict[uniq_skill] = self.skills.count(uniq_skill)
        sorted_dict = sorted(self.skills_dict.items(), key=lambda x: x[1], reverse=True)
        with open('skills.txt', 'w') as skills_list:
            for skill in sorted_dict:
                print((skill), file = skills_list)
        print(sorted_dict)
        return self.skills_dict

#if __name__ == '__main___':

user_input = User_input()
inputed_data = user_input.get_input()
href_data = Get_href(inputed_data[0], inputed_data[1])
get_links_data = href_data.get_all_links()
get_required_skills = Get_required_skills(get_links_data)
required_skills = get_required_skills.get_skills()
skills_counted = Skills_count(required_skills)
skills_counted.skills_count()
