# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .authentication import AuthenticationTestMixin
from .content import ContentTestMixin
from .forms import FormTestMixin
from .navigation import NavigationTestMixin


BROWSER_CHOICES = {
    'android': webdriver.Android,
    'chrome': webdriver.Chrome,
    'edge': webdriver.Edge,
    'firefox': webdriver.Firefox,
    'ie': webdriver.Ie,
    'opera': webdriver.Opera,
    'phantomjs': webdriver.PhantomJS,
    'safari': webdriver.Safari,
}

BROWSER = BROWSER_CHOICES[os.getenv('TEST_BROWSER', 'phantomjs').lower()]


class SeleniumLiveTestCase(AuthenticationTestMixin,
                           ContentTestMixin,
                           FormTestMixin,
                           NavigationTestMixin,
                           StaticLiveServerTestCase):

    # Fire up the web browser (via Selenium)
    @classmethod
    def setUpClass(cls):
        super(SeleniumLiveTestCase, cls).setUpClass()
        cls.browser = BROWSER()

    # Tear down the Selenium web browser
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleniumLiveTestCase, cls).tearDownClass()
