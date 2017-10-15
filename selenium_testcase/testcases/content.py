# -*- coding: utf-8 -*-

from __future__ import absolute_import

from .utils import dom_contains, wait_for


class ContentTestMixin:

    # Assert that the DOM contains the given text
    def should_see_immediately(self, text):
        self.assertTrue(dom_contains(self.browser, text))

    # Repeatedly look for the given text until it appears (or we give up)
    @wait_for
    def should_see(self, text):
        """ Wait for text to appear before raising assertion. """
        return self.should_see_immediately(text)

    @wait_for
    def has_title(self, title):
        """ Assert when page title does not match. """
        self.assertEqual(self.browser.title, title)
