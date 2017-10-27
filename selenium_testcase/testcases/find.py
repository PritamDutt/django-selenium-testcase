# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf import settings

from selenium.common.exceptions import NoSuchElementException


class FindTestMixin:

    # exit to debugger on missing element
    pdb_on_missing = getattr(
        settings, 'SELENIUM_TESTCASE_PDB_ON_MISSING', False)

    # dump page text on missing element
    text_on_missing = getattr(
        settings, 'SELENIUM_TESTCASE_TEXT_ON_MISSING', False)

    # dump png image uri on missing element
    png_on_missing = getattr(
        settings, 'SELENIUM_TESTCASE_PNG_ON_MISSING', False)

    def find_element(self, search_list, *args, **kwargs):
        """ Traverse a search list looking for elements. """

        # construct error message string just in case
        message = "Unable to find element, tried:\n"

        for method, pattern in search_list:

            # format the string as necessary
            # ignore index out of range values
            try:
                value = pattern.format(*args)
            except IndexError:
                continue

            # add method and value about to try
            message += "{}: {}\n".format(method, value)

            # try each of the patterns in order
            try:
                element = self.browser.find_element(method, value)
            except NoSuchElementException:
                pass
            else:
                return element

        # dump raw page text to exception message
        if kwargs.get('text', self.text_on_missing):
            message += "---\n" + self.get_visible_text() + "\n---\n"

        # dump image data link to exception message
        if kwargs.get('png', self.png_on_missing):
            message += "---\n" + self.get_image_uri() + "\n---\n"

        # exit to pdb if flag is set
        if kwargs.get('pdb', self.pdb_on_missing):
            import pdb
            pdb.set_trace()

        # raise the exception if we get this far
        raise NoSuchElementException(message)
