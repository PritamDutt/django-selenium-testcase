# -*- coding: utf-8 -*-

from __future__ import absolute_import

from ..testcases import SeleniumLiveTestCase


class AuthenticationTestCase(SeleniumLiveTestCase):

    def setUp(self):
        self.create_users()

    def test_regular_user_login(self):
        """ Test that you can login as user. """
        self.login("user", "user")
        self.should_see("This is your profile, user.")

    def test_admin_user_login(self):
        """ Test that you can login as admin. """
        self.login("admin", "admin")
        self.should_see("This is your profile, admin.")

    def test_admin_user_login_with_redirect(self):
        """ Test that you can login as admin. """
        self.get_page("/")
        self.at_page("/")
        self.login("admin", "admin", "/admin/")
        self.at_page("/admin/")
        self.should_see("Django administration")
