import asyncio
import requests
from collections import Counter
from bs4 import BeautifulSoup
from aiohttp import ClientSession


def get_user_input() -> tuple:
    """
    get user's input for area code and keyword
    return tuple with user inputed data.
    """
    area = input('Please enter an area code: ')
    keyword = input('Please enter a search query: ')
    return area, keyword


def get_joblist_page_url(area: int, keyword: str, page_number: int) -> str:
    """Get url for pages with jobs from
        paginated search results for area and keyword"""
    url_base = ['https://spb.hh.ru/search/vacancy?',
                '&salary=&clusters=true&',
                '&ored_clusters=true&enable_snippets=true&',
                '&hhtmFrom=vacancy_search_list']
    url_area = 'area=' + str(area)
    url_text = 'text=' + keyword
    url_page = 'page='
    url = str(url_base[0] + url_text + url_base[1] + url_area + url_base[2] \
              + url_page + str(page_number) + url_base[3])
    return url


def find_how_many_pages_with_jobs_urls(area: int,
                                       keyword: str,
                                       session: requests.Session) -> int:
    """
    Scrap first page for requested area and keyword.
    Find how many pages with job's links are returned.
    Return pages number integer
    """
    print('Calculating web-pages number')
    url = get_joblist_page_url(area, keyword, 0)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    request_page = session.get(url=url,
                               headers = headers)
    html = request_page.text
    soup = BeautifulSoup(html, 'lxml')
    page_urls = soup.find_all('a', class_='bloko-button')
    try:
        page_number = int(page_urls[len(page_urls) - 2].string)
    except ValueError:
        page_number = 0

    print(f'Found {page_number + 1} pages with job urls')
    return page_number

def skills_count(skills_list: list) -> dict:
    """
    Count skills in a list.
    Return dictionary where: skill as key; quantity as keyvalue.
    """
    cnt = Counter()
    for skill in skills_list:
        cnt[skill] += 1
    return cnt

def write_counted_skills_into_file(counted_skills: dict) -> None:
    """Write counted skills into txt file"""
    sorted_counted_skills = sorted(counted_skills.items(),
                                   key=lambda x: x[1],
                                   reverse=True)
    with open('skills.txt', 'w') as skills_file:
        for skill in sorted_counted_skills:
            print((skill), file = skills_file)

async def from_jobslist_page_get_all_urls(list_url: str,
                                          session: ClientSession) -> list:
    """
    Request web page with list of jobs. Get html source from the page.
    Find all job urls in the html source. Return list with the job urls.
    """
    print('Getting HTML-code from list page... %s' % list_url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    request_page = await session.request(method='GET',
                                         url=list_url,
                                         headers = headers)
    html = await request_page.text()
    jobs_urls_list = []
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', class_='serp-item__title')
    for url in urls:
        job_link = url.get('href').split()
        jobs_urls_list.append(job_link[0])
    return jobs_urls_list

async def from_jobdetails_page_get_all_skills(details_url: str,
                                              session: ClientSession) -> list:
    """
    Request web page with job's details. Get html source from the page.
    Find additional skills required for job in the html source.
    Return list with the requeired additional skills.
    """
    print('Getting HTML-code from details page... %s' % details_url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    request_page = await session.request(method='GET',
                                         url=details_url,
                                         headers = headers)
    html = await request_page.text()
    skills_list = []
    soup = BeautifulSoup(html, 'lxml')
    skills = soup.find_all('span',
                           class_='bloko-tag__section bloko-tag__section_text')
    for skill in skills:
        skills_list.append(skill.text)
    return skills_list

async def from_joblist_page_get_all_skills(listpage_url: str) -> list:
    """
    Get all job urls from web page with list of jobs. For every job details url
    get skills required for the jobs. Return skills for all the jobs as a list.
    """
    async with ClientSession() as session:
        skills_list = []
        raw_skills_list = []
        get_skills_from_joblist_tasks = []
        details_urls_list = await from_jobslist_page_get_all_urls(listpage_url, session)
        for details_url in details_urls_list:
            get_skills_from_details_url_task = asyncio.create_task(
                from_jobdetails_page_get_all_skills(details_url,
                                                    session)
            )
            get_skills_from_joblist_tasks.append(get_skills_from_details_url_task)
        raw_skills_list = await asyncio.gather(*get_skills_from_joblist_tasks,
                                               return_exceptions=True)
    for skills in raw_skills_list:
        skills_list.extend(skills)
    return skills_list

async def from_all_joblist_pages_get_skills(area: int,
                                            keyword: str,
                                            pages_number: int) -> list:
    """
    Get all web pages with lists of jobs according to area code and ketword.
    For all web pages with lists of jobs get additional skills required.
    Return skills required for jobs as a list.
    """
    get_skills_from_all_pages_tasks = []
    for list_page_number in range(pages_number):
        list_page_url = get_joblist_page_url(area, keyword, list_page_number)
        get_one_joblist_skills_task = asyncio.create_task(
            from_joblist_page_get_all_skills(list_page_url)
        )
        get_skills_from_all_pages_tasks.append(get_one_joblist_skills_task)
    raw_skills_list = await asyncio.gather(*get_skills_from_all_pages_tasks,
                                          return_exceptions=True)
    skills_list = []
    for skills in raw_skills_list:
        skills_list.extend(skills)
    return skills_list


def main(area=None, keyword='') -> None:
    """
    Main function. Get user input for search. Find how many pages with job urls
    is exists. For all web pages with job urls find required skills.
    Count required skills. Write counted skills into file.
    """
    if not area or keyword:
        user_input = get_user_input()
        area = user_input[0]
        keyword = user_input[1]
    with requests.Session() as session:
        pages_number = find_how_many_pages_with_jobs_urls(area,
                                                            keyword,
                                                            session)
    skills = asyncio.run(from_all_joblist_pages_get_skills(area,
                                               keyword,
                                               pages_number))
    counted_skills = skills_count(skills)
    write_counted_skills_into_file(counted_skills)

if __name__ == '__main__':
    main()
