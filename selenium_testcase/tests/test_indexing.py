# -*- coding: utf-8 -*-

from __future__ import absolute_import

from selenium.common.exceptions import NoSuchElementException

from ..testcases import SeleniumLiveTestCase


class IndexingTestCase(SeleniumLiveTestCase):

    test_templates = [
        (r'^$', 'indexing.html'),
        (r'^nav_1/$', 'nav_1.html'),
        (r'^nav_2/$', 'nav_2.html')]

    def test_no_index(self):
        """ Test default with no indexing.  Takes first button. """
        self.get_page("/")
        self.title_should_be("Indexing Test")
        self.click_button('mybutton')
        self.title_should_be("Navigation 1")

    def test_first_button(self):
        """ Test button index=0 """
        self.get_page("/")
        self.title_should_be("Indexing Test")
        self.click_button('mybutton', index=0)
        self.title_should_be("Navigation 1")

    def test_second_button(self):
        """ Test button index=1 """
        self.get_page("/")
        self.title_should_be("Indexing Test")
        self.click_button('mybutton', index=99)
        self.title_should_be("Navigation 2")

    def test_missing_button(self, index=1, timeout=1):
        """ Test button index=2 """
        self.get_page("/")
        self.title_should_be("Indexing Test")
        self.assertRaises(
            NoSuchElementException,
            self.click_button, 'mybutton', index=2, timeout=1)
