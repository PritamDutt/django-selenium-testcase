# -*- coding: utf-8 -*-

from __future__ import absolute_import

from selenium.common.exceptions import NoSuchElementException


class FindTestMixin:

    # exit to debugger on missing element
    pdb_on_missing = False

    def find_element(self, search_list, *args, **kwargs):
        """ Traverse a search list looking for elements. """

        # dump a screen shot to a file
        screendump = kwargs.get('screendump', None)
        if screendump:
            self.browser.get_screenshot_as_file(screendump)

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

        # exit to pdb if flag is set
        if kwargs.get('pdb', self.pdb_on_missing):
            import pdb
            pdb.set_trace()

        # raise the exception if we get this far
        raise NoSuchElementException(message)
