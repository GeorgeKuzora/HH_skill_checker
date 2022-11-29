import re
import subprocess
import requests
from unittest import TestCase
from hh_webscraping.main import check_if_page_contains_jobs_urls, from_all_details_pages_get_skills, from_all_list_pages_get_jobs_urls, from_details_page_html_get_skills, from_jobdetails_page_get_html_text, from_joblist_page_get_html_text, from_list_page_html_get_jobs_urls, get_joblist_page_url, get_user_input, main, skills_count, write_counted_skills_into_file
from hh_webscraping.test.test_html_pages import page_with_links, \
   page_without_links, page_with_skills


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


class TestRequestsFunctions(TestCase):
   """Test functions that make http requests and return information from web pages"""
   def setUp(self) -> None:
      self.listpage_url = 'https://spb.hh.ru/search/vacancy?text=python&from=suggest_post&area=2'
      self.detailspage_url = 'https://spb.hh.ru/vacancy/72232525?from=vacancy_search_list&query=python'
      self.session = requests.Session()
      return super().setUp()

   def test_from_joblist_page_get_html_text(self):
      response = from_joblist_page_get_html_text(self.listpage_url,
                                                 self.session)
      self.assertTrue(response != None)
      self.assertRegex(response, '<!DOCTYPE html>')
      self.assertEqual(len(re.findall('serp-item__title', response)), 40)  # 100 in case we use selenium

   def test_from_jobdetails_page_get_html_text(self):
      response = from_jobdetails_page_get_html_text(self.detailspage_url,
                                                    self.session)
      self.assertTrue(response != None)
      self.assertRegex(response, '<!DOCTYPE html>')


class TestParserFunctions(TestCase):
    """Test funcrions that uses parser engine to itearte over HTML code"""
    def setUp(self) -> None:
        web_page_with_links = 'https://spb.hh.ru/search/vacancy?text=python&salary=&clusters=true&area=2&ored_clusters=true&enable_snippets=true&page=0&hhtmFrom=vacancy_search_list'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
        self.request_page = requests.get(web_page_with_links, headers = headers)
        return super().setUp()

    def test_check_if_page_contains_jobs_urls(self):
       response_true = check_if_page_contains_jobs_urls(page_with_links())
       response_false = check_if_page_contains_jobs_urls(page_without_links())
       self.assertTrue(response_true)
       self.assertFalse(response_false)

    def test_from_list_page_html_get_jobs_urls(self):
       response = from_list_page_html_get_jobs_urls(page_with_links())
       web_page_response = from_list_page_html_get_jobs_urls(self.request_page.text)
       self.assertEqual(len(response), 1)
       self.assertGreaterEqual(len(web_page_response), 20)  # 50 in case we use Selenium

    def test_from_details_page_html_get_skills(self):
       response = from_details_page_html_get_skills(page_with_skills())
       self.assertEqual(len(response), 5)


class TestRequestMultiplePagesFunctions(TestCase):
   """Test functions that request multiple web pages"""
   def setUp(self) -> None:
      self.area = 2
      self.query = "flask"
      self.session = requests.Session()
      return super().setUp()

   def test_from_all_list_pages_get_jobs_urls(self):
      response = from_all_list_pages_get_jobs_urls(self.area,
                                                   self.query,
                                                   self.session)
      self.assertGreaterEqual(len(response), 1)

   def test_from_all_details_pages_get_skills(self):
      details_pages_urls_list = from_all_list_pages_get_jobs_urls(self.area,
                                                                  self.query,
                                                                  self.session)
      response = from_all_details_pages_get_skills(details_pages_urls_list,
                                                   self.session)
      self.assertGreaterEqual(len(response), 1)

   def test_main(self):
      main(self.area, self.query)
      with open('skills.txt', 'r') as skills_file:
         data = skills_file.read()
      subprocess.call('rm skills.txt', shell=True)
      data_list = data.split('\n')
      data_list.pop()
      self.assertGreater(len(data_list), 3)


if __name__ == '__main__':
    unittest.main()
