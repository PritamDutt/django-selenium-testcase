# -*- coding: utf-8 -*-

from __future__ import absolute_import

from selenium.common.exceptions import NoSuchElementException

from ..testcases import SeleniumLiveTestCase


class NavigationTestCase(SeleniumLiveTestCase):

    test_templates = [
        (r'^nav_1/$', 'nav_1.html'),
        (r'^nav_1/nav_2/$', 'nav_2.html')
    ]

    def test_get_page(self):
        """ Test that you can traverse the page tree. """
        self.get_page("/nav_1/")
        self.title_should_be("Navigation 1")
        self.title_should_contain("1")
        self.should_see("This is nav 1.")
        self.get_page("/nav_1/nav_2/")
        self.should_see("This is nav 2.")

    def test_get_page_by_name(self):
        """ Test that you can reverse a named page. """
        self.get_page_by_name("user_profile")
        self.should_see("This is your profile, .")

    def test_get_bad_page(self):
        """ Test that /bogus/ is not found. """
        self.get_page("/bogus/")
        self.should_see("Not Found")
        self.should_see(
            "The requested URL /bogus/ was not found on this server.")

    def test_missing_content_with_retry(self):
        """ Test retry for missing content, LONG RETRIES! """
        self.get_page("/nav_1/")
        self.should_not_see("This is nav 2.")
        self.url_should_not_contain("nav_2")
        self.title_should_not_be("Navigation 2")
        self.title_should_not_contain("2")
        self.assertRaises(
            NoSuchElementException, self.click_button, "not_there_dude")
        self.not_at_page("/nav_2/")
