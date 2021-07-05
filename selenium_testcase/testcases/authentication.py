from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

from .utils import wait_for


class AuthenticationTestMixin:
    login_url = "/accounts/login/"
    login_username_field = "login"
    login_password_field = "password"
    login_button = "Sign In"
    user_model = get_user_model()

    # Admin login
    admin_site_url = "/admin/login/"
    admin_login_username_field = "username"
    admin_login_password_field = "password"
    admin_login_button = "Log in"

    @wait_for
    def should_be_logged_in_as(self, username):
        """ See if this user is logged in.  """
        user = self.user_model.objects.get(username=username)
        for session in Session.objects.all():
            if str(user.id) == session.get_decoded().get("_auth_user_id"):
                return True
        self.fail("User '{}' is not logged in.".format(username))

    def login(self, username, password, next_url=None):

        # grab the login page
        if next_url:
            self.get_page("{}?next={}".format(self.login_url, next_url))
        else:
            self.get_page(self.login_url)

        self.set_input(self.login_username_field, username)
        self.set_input(self.login_password_field, password)
        self.click_button(self.login_button)
        self.should_be_logged_in_as(username)

    def admin_site_login(self, username, password, next_url=None):
        """Login the user to admin site"""
        # grab the login page
        if next_url:
            self.get_page("{}?next={}".format(self.admin_site_url, next_url))
        else:
            self.get_page(self.admin_site_url)

        self.set_input(self.admin_login_username_field, username)
        self.set_input(self.admin_login_password_field, password)
        self.click_button(self.admin_login_button)
        self.should_be_logged_in_as(username)

    def create_users(self):
        """ Create an admin/admin and user/user test users. """
        self.user_model.objects.filter(
            username="admin"
        ).exists() or self.user_model.objects.create_superuser(
            "admin", "admin@example.com", "admin"
        )
        self.user_model.objects.filter(
            username="user"
        ).exists() or self.user_model.objects.create_user(
            "user", "user@example.com", "user"
        )

        self.admin = self.user_model.objects.filter(username="admin").first()
        self.user = self.user_model.objects.filter(username="user").first()
