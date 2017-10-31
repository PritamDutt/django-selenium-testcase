# -*- coding: utf-8 -*-

from __future__ import absolute_import

from selenium.webdriver.common.by import By

from .utils import wait_for


class FormTestMixin:

    # default search element
    form_search_list = (
        (By.ID, '{}',),
        (By.NAME, '{}',),
        (By.XPATH, '//form[@action="{}"]',),
        (By.XPATH, '//form[@name="{}"]',),
        (By.XPATH, '//form',),
    )

    @wait_for
    def get_form(self, *args, **kwargs):
        """ Return form element or None. """
        return self.find_element(
            self.form_search_list, *args, **kwargs)

    input_search_list = (
        (By.ID, '{}',),
        (By.NAME, '{}',),
    )

    @wait_for
    def get_input(self, field, **kwargs):
        """ Return matching input field. """
        return self.find_element(
            self.input_search_list, field, **kwargs)

    def set_input(self, field, value, **kwargs):
        """ Clear the field and enter value. """
        element = self.get_input(field, **kwargs)
        element.clear()
        element.send_keys(value)
        return element
