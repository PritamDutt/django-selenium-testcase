# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.contrib.auth.models import User


class AuthenticationTestMixin:

    login_url = "/accounts/login/"
    login_username_field = "username"
    login_password_field = "password"
    login_button = "login"

    def login(self, username, password, next_url=None):

        # grab the login page
        if next_url:
            self.get_page("{}?next={}".format(self.login_url, next_url))
        else:
            self.get_page(self.login_url)

        self.set_input(self.login_username_field, username)
        self.set_input(self.login_password_field, password)
        self.click_button(self.login_button)

    def create_users(self):
        """ Create an admin/admin and user/user test users. """
        self.admin = User.objects.create_superuser(
            'admin', 'admin@example.com', 'admin')
        self.user = User.objects.create_user(
            'user', 'user@example.com', 'user')
