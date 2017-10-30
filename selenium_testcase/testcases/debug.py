# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import inspect

from django.conf import settings
from django.template.loader import render_to_string


class DebugTestMixin:

    """
    Add convenience debug methods to selenium test cases.

    This class manages debug logging of selenium through screenshots, html
    source, and visible text dumps. It can generate a single HTML file with a
    complete trace of the selenium execution.



    Settings:

        SELENIUM_TESTCASE_BASE_DIR:
            - The base path for created files. Default: current directory.

        SELENIUM_TESTCASE_LOGGING:
            - When true, create an HTML log file of all test case steps.
              Default: False.

    Attributes:

        selenium_base_dir - class override of SELENIUM_TESTCASE_BASE_DIR
        selenium_logging - override class override of SELENIUM_TESTCASE_LOGGING
        _selenium_log_file - private file pointer of the HTML log file

    Methods:

        render_header_log(self):
            - Process the settings and conditionally open the log file.
              Returns: None.

        render_footer_log(self):
            - Close the log file if open.  Returns: None.

        render_log(self, template):
            - Write the results from the current test frame to the log file.

        render_entry_log(self):
            - Write the results entering the current step.

        render_exit_log(self):
            - Write the results exiting the current step.

        get_screenshot_uri(self):
            - Grab the current screenshot from selenium and
              return the png as a base64 data uri string.

        get_visible_text(self):
            - Return visible text from the body element.

        get_test_frame(self):
            - Return the stack frame of the current test.

    """

    # private file handle for HTML log file
    _selenium_log_file = None

    # base path for files created by this package
    selenium_base_dir = getattr(settings, 'SELENIUM_TESTCASE_BASE_DIR', '.')

    # log to an HTML file for all tests, if true
    selenium_logging = getattr(settings, 'SELENIUM_TESTCASE_LOGGING', False)

    # templates used for log file generation
    selenium_header_template = getattr(
        settings, 'SELENIUM_TESTCASE_HEADER_TEMPLATE',
        'selenium_testcase/header.html')

    selenium_footer_template = getattr(
        settings, 'SELENIUM_TESTCASE_FOOTER_TEMPLATE',
        'selenium_testcase/footer.html')

    selenium_testcase_entry_template = getattr(
        settings, 'SELENIUM_TESTCASE_ENTRY_TEMPLATE',
        'selenium_testcase/entry.html')

    selenium_testcase_exit_template = getattr(
        settings, 'SELENIUM_TESTCASE_EXIT_TEMPLATE',
        'selenium_testcase/exit.html')

    def render_header_log(self):
        """
        Process settings and conditionally open the HTML log file.

        The filename is base on the TestCase id().  For example:
        selenium_testcase.tests.test_forms.FormTestCase.test_form.html.

        """

        if self.selenium_logging:

            # open the file
            file = os.path.join(self.selenium_base_dir, self.id() + '.html')
            self._selenium_log_file = open(file, "w")

            # render the header
            html = render_to_string(
                self.selenium_header_template,
                {'id': self.id(), 'description': self.__doc__})

            # write it to the file
            self._selenium_log_file.write(html)

    def render_footer_log(self):
        """
        Close the log file if open.
        """

        # clean up the log file
        if self._selenium_log_file:

            # render the footer
            html = render_to_string(
                self.selenium_footer_template,
                {'id': self.id(), 'description': self.__doc__})

            # write it to the file
            self._selenium_log_file.write(html)

    def render_log(self, template):
        """
        Write the results from the current test frame to the log file.
        """

        # only write to the log file if it exists
        if self._selenium_log_file:

            id = self.id()
            description = self.shortDescription()

            # grab the stack frame info from test_* method
            (obj, filename, lineno, function, code_context, index) \
                = self.get_test_frame()

            # render the test case debug
            html = render_to_string(
                template, {
                    'id': id,
                    'description': description,
                    'filename': filename,
                    'lineno': lineno,
                    'function': function,
                    'code_context': code_context,
                    'index': index,
                    'png': self.get_image_uri(),
                    'text': self.get_visible_text()})

            # write it to the file
            self._selenium_log_file.write(html)

    def render_entry_log(self):
        """
        This template renders before the step.
        """
        self.render_log(self.selenium_testcase_entry_template)

    def render_exit_log(self):
        """
        This template renders after the step.
        """
        self.render_log(self.selenium_testcase_exit_template)

    def get_image_uri(self):
        """ Return a data uri with a base64 embedded screenshot. """
        return "data:image/png;base64," + \
            self.browser.get_screenshot_as_base64()

    def get_visible_text(self):
        """ Return visible text from the body element. """
        return self.browser.find_element_by_xpath("//body").text

    def get_test_frame(self):
        """ Return the stack frame of the current test.

        This method extracts the test method name (i.e. 'test_forms') from the
        TestCase id() and traverses up the stack frame until it finds a
        matching method name. Returns the frame tuple or None.

        stack frame is (obj, filename, lineno, function, code_context, index).
        """

        # get function from end of unittest id()
        target = self.id().split('.')[-1]

        # traverse frames until function name is found
        for frame in inspect.stack():
            if frame[3] == target:
                return frame
        return None
