# -*- coding: utf-8 -*-

from __future__ import absolute_import


class FormTestMixin:

    def set_input(self, field, value):
        inputs = self.browser.find_elements_by_name(field)
        for input in inputs:
            if input.is_displayed():
                input.send_keys(value)
                return
