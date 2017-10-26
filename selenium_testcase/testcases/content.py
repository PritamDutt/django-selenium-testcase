# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .utils import wait_for

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class ContentTestMixin:

    content_search_list = (
        (By.XPATH,
         '//*[contains(normalize-space(.), "{}") '
         'and not(./*[contains(normalize-space(.), "{}")])]',),
    )

    def should_see_immediately(self, text, **kwargs):
        """ Assert that DOM contains the given text. """
        self.find_element(
            self.content_search_list, text, text, **kwargs)

    @wait_for
    def should_see(self, text):
        """ Wait for text to appear before testing assertion. """
        return self.should_see_immediately(text)

    def should_not_see(self, text):
        """ Wait for text to not appear before testing assertion. """
        self.assertRaises(NoSuchElementException, self.should_see, text)

    @wait_for
    def title_should_be(self, title):
        """ Assert that page title matches. """
        self.assertEqual(self.browser.title, title)

    def title_should_not_be(self, title):
        """ Assert when page title does not match. """
        self.assertRaises(AssertionError, self.title_should_be, title)

    @wait_for
    def title_should_contain(self, text):
        """ Assert that page title contains text. """
        self.assertIn(text, self.browser.title)

    def title_should_not_contain(self, text):
        """ Assert that page title does not contain text. """
        self.assertRaises(AssertionError, self.title_should_contain, text)
