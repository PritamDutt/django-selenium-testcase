# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ..testcases import SeleniumLiveTestCase


class DebugTestCase(SeleniumLiveTestCase):

    test_templates = [(r'', 'test.html')]

    def test_debug(self):
        """
        Test a simple home page.
        """
        self.get_page("/")
        self.title_should_be("Test")
        self.should_see("This is a test.")
        self.should_see("This is a")
        self.should_see("is a test.")
        self.should_see("is a")
        self.should_see("The quick brown")
