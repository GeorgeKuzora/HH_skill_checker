import unittest
import aiounittest
import asyncio
import subprocess
import requests
from unittest import TestCase
from aiounittest import AsyncTestCase
from aiohttp import ClientSession
from hh_webscraping.main import find_how_many_pages_with_jobs_urls, \
   from_all_joblist_pages_get_skills, \
   from_jobdetails_page_get_all_skills, from_joblist_page_get_all_skills, \
   get_user_input, get_joblist_page_url, main, write_counted_skills_into_file, \
   skills_count, from_jobslist_page_get_all_urls


class TestBaseFunctions(TestCase):
   """Test functions dependened on user input"""
   def setUp(self) -> None:
      self.area = 2
      self.query = "python"
      self.page_number = 0
      self.skills_list = ['django', 'sql', 'django', 'java', 'django', 'sql']
      self.counted_skills_dict = {'sql': 2, 'django': 3, 'java': 1}
      return super().setUp()

   def test_get_input(self):
       result = get_user_input()
       self.assertEqual(result, ('2', 'python'))

   def test_get_joblist_page_url(self):
      url = get_joblist_page_url(self.area, self.query, self.page_number)
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
      response = requests.get(url, headers = headers)
      self.assertEqual(response.status_code, 200)

   def test_skills_count(self):
      counted_skills = skills_count(self.skills_list)
      self.assertEqual(counted_skills, {'django': 3, 'sql': 2, 'java': 1})
      self.assertEqual(len(counted_skills), 3)

   def test_write_counted_skills_into_file(self):
      write_counted_skills_into_file(self.counted_skills_dict)
      with open('skills.txt', 'r') as skills_file:
         data = skills_file.read()
      subprocess.call('rm skills.txt', shell=True)
      data_list = data.split('\n')
      data_list.pop()
      self.assertEqual(len(data_list), 3)


class TestParserFunctions(AsyncTestCase):
    """Test funcrions that uses requests and parser engines to itearte over HTML code"""
    def setUp(self) -> None:
        self.area = 2
        self.query = "python"
        self.main_query = "японский язык"
        self.web_page_with_links = 'https://spb.hh.ru/search/vacancy?text=python&salary=&clusters=true&area=2&ored_clusters=true&enable_snippets=true&page=0&hhtmFrom=vacancy_search_list'
        self.web_page_details = 'https://spb.hh.ru/vacancy/73038222?from=vacancy_search_list&query=python'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        self.request_page = requests.get(self.web_page_with_links, headers = headers)
        return super().setUp()

    def test_find_how_many_pages_with_jobs_urls(self):
       with requests.Session() as session:
           page_number = find_how_many_pages_with_jobs_urls(self.area,
                                                         self.query,
                                                         session)
       self.assertGreaterEqual(page_number, 1)

    async def test_from_jobslist_page_get_all_urls(self):
        async with ClientSession() as session:
            response = await from_jobslist_page_get_all_urls(self.web_page_with_links,
                                                       session)
        self.assertGreaterEqual(len(response), 20)  # 50 in case we use Selenium

    async def test_from_jobdetails_page_get_all_skills(self):
        async with ClientSession() as session:
            response = await from_jobdetails_page_get_all_skills(self.web_page_details,
                                                       session)
        self.assertEqual(len(response), 5)

    async def test_from_joblist_page_get_all_skills(self):
        response = await from_joblist_page_get_all_skills(self.web_page_with_links)
        self.assertGreaterEqual(len(response), 9)
        self.assertIn('Python', response)

    async def test_from_all_joblist_pages_get_skills(self):
        response = await from_all_joblist_pages_get_skills(self.area,
                                                           self.query,
                                                           5)

        self.assertGreaterEqual(len(response), 50)
        self.assertIn('Python', response)

    def test_main(self):
        main(self.area, self.main_query,)
        with open('skills.txt', 'r') as skills_file:
           data = skills_file.read()
        subprocess.call('rm skills.txt', shell=True)
        data_list = data.split('\n')
        self.assertGreaterEqual(len(data_list), 10)


if __name__ == '__main__':
    unittest.main()
