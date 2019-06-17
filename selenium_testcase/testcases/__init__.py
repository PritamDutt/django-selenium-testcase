# -*- coding: utf-8 -*-

from __future__ import absolute_import
from importlib import reload

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import clear_url_caches

from selenium.webdriver.chrome.options import Options

from ..settings import TEST_DRIVER, TEST_BROWSER
from ..settings import SELENIUM_WINDOW_SIZE

from .authentication import AuthenticationTestMixin
from .content import ContentTestMixin
from .debug import DebugTestMixin
from .find import FindTestMixin
from .forms import FormTestMixin
from .navigation import NavigationTestMixin
from .utils import reload_urlconf

# this is absolute due to reload
from selenium_testcase import urls


class SeleniumLiveTestCase(AuthenticationTestMixin,
                           ContentTestMixin,
                           DebugTestMixin,
                           FindTestMixin,
                           FormTestMixin,
                           NavigationTestMixin,
                           StaticLiveServerTestCase):

    # list of path, template tuples added to urlconf
    test_templates = []

    # Fire up the web browser (via Selenium)
    @classmethod
    def setUpClass(cls):
        """
        SeleniumLiveTestCase setUpClass

        This method starts a LiveTestBrowser for selenium testing and a web
        browser session specified by the TEST_BROWSER environment variable.
        The default is phantomjs. It also looks for a "test_templates"
        list of path/template tuples in the derived TestCase class and
        adds TemplateView views to urlconf.

        test_templates = [
            (r'^nav_1/$', 'nav_1.html'),
            (r'^nav_1/nav_2/$', 'nav_2.html')
        ]


        """

        # pass template tuple as a settings override to urls.py
        cls._overridden_settings = {
            'SELENIUM_TESTCASE_TEMPLATES': cls.test_templates}
        super(SeleniumLiveTestCase, cls).setUpClass()

        # Launch the browser session. If the browser is non-headless Chrome,
        # launch it with the "--no-sandbox" option to prevent problems when
        # running in a containerized Travis CI build.
        # https://docs.travis-ci.com/user/chrome#Sandboxing
        # https://github.com/travis-ci/travis-ci/issues/8836
        if TEST_BROWSER == 'chrome':
            options = Options()
            options.add_argument('--no-sandbox')
            cls.browser = TEST_DRIVER(chrome_options=options)
        else:
            cls.browser = TEST_DRIVER()

        # configure the window size
        (width, height) = SELENIUM_WINDOW_SIZE.lower().split('x')
        cls.browser.set_window_size(int(width), int(height))

        # reload selenium_testcase.urls to fetch the new setting
        # clear url cache, and reload urlconf
        reload(urls)
        clear_url_caches()
        reload_urlconf()

    def __init__(self, *args, **kwargs):
        super(SeleniumLiveTestCase, self).__init__(*args, **kwargs)
        self.addCleanup(DebugTestMixin.render_footer_log, self)
        self.render_header_log()

    # Tear down the Selenium web browser
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SeleniumLiveTestCase, cls).tearDownClass()
