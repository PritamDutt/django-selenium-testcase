# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .utils import dom_contains, wait_for


class ContentTestMixin:

    def should_see_immediately(self, text):
        """ Assert that DOM contains the given text. """
        self.assertTrue(dom_contains(self.browser, text))

    @wait_for
    def should_see(self, text):
        """ Wait for text to appear before testing assertion. """
        return self.should_see_immediately(text)

    def should_not_see(self, text):
        """ Wait for text to not appear before testing assertion. """
        self.assertRaises(AssertionError, self.should_see, text)

    @wait_for
    def has_title(self, title):
        """ Assert that page title matches. """
        self.assertEqual(self.browser.title, title)

    def has_not_title(self, title):
        """ Assert when page title does not match. """
        self.assertRaises(AssertionError, self.has_title, title)

    @wait_for
    def title_contains(self, text):
        """ Assert that page title contains text. """
        self.assertIn(text, self.browser.title)

    def title_does_not_contain(self, text):
        """ Assert that page title does not contain text. """
        self.assertRaises(AssertionError, self.title_contains, text)
