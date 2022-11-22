from unittest import TestCase, mock
from hh_webscraping import main
from hh_webscraping.main import GetRequiredSkills, UserInput, GetHref
from hh_webscraping.test import test_html_pages


class TestUserInput(TestCase):
   """Test UserInput class"""
   def test_get_input(self):
       self.result = UserInput.get_input(self)
       self.assertEqual(self.result, ('2', 'python'))


class TestGetHref(TestCase):
   """Test GetHref class"""
   def setUp(self) -> None:
      """
      Variables initialisation
      self.url -- string, path to the test html page
      self.html_with_links -- string, html text with link to a job
      self.html_without_links -- string, html text without links to jobs
      """
      self.url = 'https://spb.hh.ru/search/vacancy?text=python&from=suggest_post&area=2'
      self.html_with_links = test_html_pages.page_with_links()
      self.html_without_links = test_html_pages.page_without_links()
      return super().setUp()

   def test_get_html(self):
      """test if mehtod return data from url"""
      requested_page = GetHref.get_html(self, self.url)
      self.assertTrue(requested_page != None)

   def test_is_empty(self):
      """test if method rerurn True if required links doesn't exist in html code"""
      links_exist = GetHref.is_empty(self, self.html_with_links)
      links_does_not_exist = GetHref.is_empty(self, self.html_without_links)
      self.assertFalse(links_exist)
      self.assertTrue(links_does_not_exist)

   def test_get_offers_links(self):
      """test if method returns list with all job links from page"""
      link_list = GetHref.get_offers_links(self, self.html_with_links)
      self.assertEqual(len(link_list), 1)

   # def test_get_all_links(self):
   #    """test if method returns list with all links"""
   #    all_links = GetHref.get_all_links(self)
   #    self.assertTrue(len(all_links) >= 1)


class TestGetRequiredSkills(TestCase):
   """Test GetRequiredSkills class"""
   def setUp(self):
      """
      Variables initialisation
      self.url -- string, path to the test html page
      """
      self.url = 'https://spb.hh.ru/search/vacancy?text=python&from=suggest_post&area=2'
      return super().setUp()


   def test_get_html(self):
      """test if mehtod return data from url"""
      requested_page = GetRequiredSkills.get_html(self, self.url)
      self.assertTrue(requested_page != None)



if __name__ == '__main__':
    unittest.main()
