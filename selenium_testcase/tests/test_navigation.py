# -*- coding: utf-8 -*-

from __future__ import absolute_import


from ..testcases import SeleniumLiveTestCase


class NavigationTestCase(SeleniumLiveTestCase):

    test_templates = [
        (r'^nav_1/$', 'nav_1.html'),
        (r'^nav_1/nav_2/$', 'nav_2.html')
    ]

    def test_get_page(self):
        """ Test that you can traverse the page tree. """
        self.get_page("/nav_1/")
        self.should_see("This is nav 1.")
        self.get_page("/nav_1/nav_2/")
        self.should_see("This is nav 2.")
