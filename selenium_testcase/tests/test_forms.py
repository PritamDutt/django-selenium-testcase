# -*- coding: utf-8 -*-

from __future__ import absolute_import

from selenium.common.exceptions import NoSuchElementException

from ..testcases import SeleniumLiveTestCase


class FormTestCase(SeleniumLiveTestCase):

    test_templates = [(r'', 'form.html')]

    def test_get_form(self):
        """
        Test getting a form.
        """
        self.get_page("/")
        self.has_title("Form Test")
        self.get_form()
        self.get_form("myForm")

    def test_form(self):
        """
        Test submitting a form with inputs and dropdown.
        """
        self.get_page("/")
        self.has_title("Form Test")
        self.set_input("firstname", "Donald")
        self.set_input("lastname", "Duck")
        self.select_dropdown("cars", "Fiat")
        self.click_button("Submit")
        self.url_should_contain("firstname=Donald")
        self.url_should_not_contain("Mickey")
        self.url_should_contain("lastname=Duck")
        self.url_should_not_contain("Mouse")


class MissingFormTestCase(SeleniumLiveTestCase):

    def test_missing_form(self):
        """ Look for a form that does not exist. """
        self.get_page("/")
        self.assertRaises(NoSuchElementException, self.get_form)
