# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ..testcases import SeleniumLiveTestCase


class AuthenticationTestCase(SeleniumLiveTestCase):

    def setUp(self):
        self.create_users()

    def test_admin_user_login(self):
        """ Test that you can login as user. """

        self.login("user", "user", "/")
        self.should_see("This is a test.")
