from collections import Counter
from time import time
from bs4 import BeautifulSoup
import requests


def get_user_input() -> tuple:
    """
    get user's input for area code and keyword
    return tuple with user inputed data
    """
    area = input('Please enter an area code: ')
    query = input('Please enter a search query: ')
    return area, query


def get_joblist_page_url(area: int, query: str, page_number: int) -> str:
    """Get url for pages with jobs from
        paginated search results for area and keyword"""
    url_base = ['https://spb.hh.ru/search/vacancy?',
                '&salary=&clusters=true&',
                '&ored_clusters=true&enable_snippets=true&',
                '&hhtmFrom=vacancy_search_list']
    url_area = 'area=' + str(area)
    url_text = 'text=' + query
    url_page = 'page='
    url = str(url_base[0] + url_text + url_base[1] + url_area + url_base[2] \
              + url_page + str(page_number) + url_base[3])
    return url

def from_joblist_page_get_html_text(list_url: str) -> str:
    """get html text from the requested jobs list page.
    IO based function"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    request_page = requests.get(list_url, headers = headers)
    print('Getting HTML-code from... %s' % list_url)
    return request_page.text

def check_if_page_contains_jobs_urls(html: str) -> bool:
    """check if job list page contains any job offer urls. Return True if yes"""
    is_urls = False
    soup = BeautifulSoup(html, 'lxml')
    _job_cards = soup.find_all('a', class_='serp-item__title')
    if _job_cards:
        is_urls = True
    return is_urls


def from_list_page_html_get_jobs_urls(html: str) -> list:
    """Get list of all jobs links from html code"""
    jobs_urls_list = []
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', class_='serp-item__title')
    for url in urls:
        job_link = url.get('href').split()
        jobs_urls_list.append(job_link[0])
    return jobs_urls_list

def from_jobdetails_page_get_html_text(details_url: str) -> str:
    """get html text from the requested jobs details page.
    IO based function"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    request_page = requests.get(details_url, headers = headers)
    print('Getting HTML-code from... %s' % details_url)
    return request_page.text

def from_details_page_html_get_skills(html: str) -> list:
    """Get list of all required skills from html code"""
    skills_list = []
    soup = BeautifulSoup(html, 'lxml')
    skills = soup.find_all('span',
                           class_='bloko-tag__section bloko-tag__section_text')
    for skill in skills:
        skills_list.append(skill.text)
    return skills_list

def skills_count(skills_list: list) -> dict:
    """Count all skills and return dictionary where key is skill, value is quantity"""
    cnt = Counter()
    for skill in skills_list:
        cnt[skill] += 1
    return cnt

def write_counted_skills_into_file(counted_skills: dict) -> None:
    """Write counted job's skills into txt file"""
    sorted_counted_skills = sorted(counted_skills.items(),
                                   key=lambda x: x[1],
                                   reverse=True)
    with open('skills.txt', 'w') as skills_file:
        for skill in sorted_counted_skills:
            print((skill), file = skills_file)

def from_all_list_pages_get_jobs_urls(area: int, query: str) -> list:
    """Get urls from all keyword search pages and return them as a list"""
    job_urls_list = []
    list_page_number = 0
    list_page_contains_urls = True
    while list_page_contains_urls:
        list_page_url = get_joblist_page_url(area, query, list_page_number)
        job_list_html = from_joblist_page_get_html_text(list_page_url)
        list_page_contains_urls = check_if_page_contains_jobs_urls(job_list_html)
        if list_page_contains_urls:
            page_job_urls_list = from_list_page_html_get_jobs_urls(job_list_html)
            job_urls_list.extend(page_job_urls_list)
            list_page_number += 1
    return job_urls_list

def from_all_details_pages_get_skills(details_pages_urls_list: list) -> list:
    """Get all skills from all details pages urls. Return them as a list"""
    skills_list = []
    for url in details_pages_urls_list:
        print('%d from %d' % (details_pages_urls_list.index(url) + 1,
                              len(details_pages_urls_list)))
        html = from_jobdetails_page_get_html_text(url)
        skills = from_details_page_html_get_skills(html)
        skills_list.extend(skills)
    return skills_list

    
def main(area=None, query=None) -> None:
    """Main function. Makes other functions in right order"""
    if not area and query:
        user_input = get_user_input()
        area = user_input[0]
        query = user_input[1]
    jobs_urls = from_all_list_pages_get_jobs_urls(area, query)
    skills = from_all_details_pages_get_skills(jobs_urls)
    counted_skills = skills_count(skills)
    write_counted_skills_into_file(counted_skills)


if __name__ == '__main__':
    main()
