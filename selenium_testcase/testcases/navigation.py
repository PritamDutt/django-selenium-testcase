# -*- coding: utf-8 -*-

from __future__ import absolute_import

from urlparse import urljoin

from django.urls import reverse
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


class NavigationTestMixin:

    def get_page(self, url):
        """ Navigate to the given url.  """
        return self.browser.get(urljoin(self.live_server_url, url))

    def get_page_by_name(self, viewname, *args, **kwargs):
        """ Navigate to the named url using django.urls.reverse(). """
        return self.browser.get(
            urljoin(self.live_server_url,
                    reverse(viewname, *args, **kwargs)))

    dropdown_search_list = (
        (By.ID, '{}',),
        (By.NAME, '{}',),
    )

    def select_dropdown(self, field, value):
        """ Select a dropdown menu on the current page. """
        dropdown = self.find_element(self.dropdown_search_list, field)
        input = Select(dropdown)
        input.select_by_visible_text(value)

    # default search for button
    button_search_list = (
        (By.ID, '{}',),
        (By.NAME, '{}',),
        (By.XPATH, '//a[text()="{}"]',),
        (By.XPATH, '//input[@value="{}"]',),
        (By.XPATH, '//button[text()="{}"]',),
        (By.XPATH, '//button[text()[contains(.,"{}")]]',),
    )

    def click_button(self, *args, **kwargs):
        """ Select a button or link with the given name.  """
        button = self.find_element(self.button_search_list, *args, **kwargs)
        button.click()

    def at_page(self, url):
        """ Assert current page is not at the given url. """
        self.assertEqual(
            urljoin(self.live_server_url, url), self.browser.current_url)

    def not_at_page(self, url):
        """ Assert current page is at the given url. """
        self.assertNotEqual(
            urljoin(self.live_server_url, url), self.browser.current_url)

    def url_should_contain(self, text):
        """ Assert if the current url DOES NOT contain the given string. """
        self.assertIn(text, self.browser.current_url)

    def url_should_not_contain(self, text):
        """ Assert if the current url DOES contain the given string. """
        self.assertNotIn(text, self.browser.current_url)
