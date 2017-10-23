# -*- coding: utf-8 -*-

from __future__ import absolute_import

from urlparse import urljoin

from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class NavigationTestMixin:

    def get_page(self, url):
        """ Navigate to the given url.  """
        return self.browser.get(urljoin(self.live_server_url, url))

    def select_dropdown(self, field, value):
        """ Select a dropdown menu on the current page. """
        input = Select(self.browser.find_element_by_name(field))
        input.select_by_visible_text(value)

    def click_button(self, button_name):
        """ Select a button or link with the given name.  """
        for xpath in [x.format(button_name) for x in [
                '//a[text()="{}"]',
                '//input[@value="{}"]',
                '//button[text()="{}"]',
                '//button[text()[contains(.,"{}")]]',
        ]]:
            try:
                buttons = self.browser.find_elements_by_xpath(xpath)
                for button in buttons:
                    if button.is_displayed():
                        button.click()
                        return
            except NoSuchElementException:
                pass

        self.assertFalse("Button not found: '{}'".format(button_name))

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
