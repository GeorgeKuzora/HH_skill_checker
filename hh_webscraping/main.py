from bs4 import BeautifulSoup
import requests
import time

# Класс служит для того чтобы получить входные данные от пользователя
class UserInput:
    """Get input data from the user
    area - in what city we want to scrap 2 Saint-Petersburg
    query - string with keyword"""
    def __init__(self):
        self.area = None
        self.query = None

    def get_input(self):
        """
        get user's input for area code and keyword
        return tuple with user inputed data
        """
        self.area = input('Please enter an area code: ')
        self.query = input('Please enter a search query: ')
        return self.area, self.query

class GetHref:
    """
    Get URLs for jobs pages, from the page with listed jobs
    return -- list
    """
    def __init__(self, area, query):
        """init for variables
        self.area -- integer, area number from UserInput
        self.query -- string, keyword form UserInput
        self.all_links -- list, will contain jobs pages links"""
        self.area = area
        self.query = query
        self.all_links = []

    def get_html(self, url):
        """Get html page text for page with listed jobs
        return string"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        request_page = requests.get(url, headers = headers)
        print('Getting HTML-code from... %s' % url)

        return request_page.text

    def is_empty(self, html):
        soup = BeautifulSoup(html, 'lxml')
        _job_cards = soup.find_all('a', class_='serp-item__title') #'div', class_='vacancy-serp-item ')
        if not _job_cards:
            return True
        elif _job_cards:
            return False

    def get_offers_links(self, html):
        """Get list of all jobs links from html code"""
        all_links = []
        soup = BeautifulSoup(html, 'lxml')
        links = soup.find_all('a', class_='serp-item__title')
        for link in links:
            _offered_link = link.get('href').split()
            all_links.append(_offered_link[0])
        return all_links


    def get_all_links(self):
        """Get url for pages with jobs from
           paginated search results for area and keyword"""
        _url_base = ['https://spb.hh.ru/search/vacancy?', '&salary=&clusters=true&', '&ored_clusters=true&enable_snippets=true&', '&hhtmFrom=vacancy_search_list']
        _url_area = 'area=' + str(self.area)
        _url_text = 'text=' + self.query
        _url_page = 'page='
        _page = 0
        all_links = []

        page_is_not_empty = True

        while page_is_not_empty:
            url = str(_url_base[0] + _url_text + _url_base[1] + _url_area + _url_base[2] + _url_page + str(_page) + _url_base[3])
#           time.sleep(.1)
            html = self.get_html(url)
            if not self.is_empty(html):
                all_links.extend(self.get_offers_links(html))
                _page += 1
            else:
                page_is_not_empty = False
        return all_links

class GetRequiredSkills:

    def __init__(self, job_offers):
        self.job_offers = job_offers
        self.skills = []
        self.description = []

    def get_html(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        request_page = requests.get(url, headers = headers)
        return request_page.text

    def get_skills(self):
        """Get all skils from jobs pages"""
        for link in self.job_offers:
            print('%d from %d' % (self.job_offers.index(link) + 1, len(self.job_offers)))
            html = self.get_html(link)
            soup = BeautifulSoup(html, 'lxml')
            skill_block = soup.find_all('span', class_='bloko-tag__section bloko-tag__section_text')
            for skill in skill_block:
                self.skills.append(skill.text)
        return self.skills

class SkillsCount:
    """Count skils"""
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

if __name__ == '__main__':

    user_input = UserInput()
    inputed_data = user_input.get_input()
    href_data = GetHref(inputed_data[0], inputed_data[1])
    get_links_data = href_data.get_all_links()
    get_required_skills = GetRequiredSkills(get_links_data)
    required_skills = get_required_skills.get_skills()
    skills_counted = SkillsCount(required_skills)
    skills_counted.skills_count()
