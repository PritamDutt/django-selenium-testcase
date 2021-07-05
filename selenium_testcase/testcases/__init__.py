from django.test import LiveServerTestCase
from django.urls import clear_url_caches
from selenium.webdriver.chrome.options import Options

from .authentication import AuthenticationTestMixin
from .content import ContentTestMixin
from .debug import DebugTestMixin
from .find import FindTestMixin
from .forms import FormTestMixin
from .navigation import NavigationTestMixin
from ..settings import SELENIUM_WINDOW_SIZE
from ..settings import TEST_DRIVER, TEST_BROWSER


class SeleniumLiveTestCase(
    AuthenticationTestMixin,
    ContentTestMixin,
    DebugTestMixin,
    FindTestMixin,
    FormTestMixin,
    NavigationTestMixin,
    LiveServerTestCase,
):
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
        if cls._overridden_settings:
            cls._overridden_settings["SELENIUM_TESTCASE_TEMPLATES"] = cls.test_templates
        else:
            # pass template tuple as a settings override to urls.py
            cls._overridden_settings = {
                "SELENIUM_TESTCASE_TEMPLATES": cls.test_templates
            }
        super(SeleniumLiveTestCase, cls).setUpClass()

        # Launch the browser session. If the browser is non-headless Chrome,
        # launch it with the "--no-sandbox" option to prevent problems when
        # running in a containerized Travis CI build.
        # https://docs.travis-ci.com/user/chrome#Sandboxing
        # https://github.com/travis-ci/travis-ci/issues/8836
        if TEST_BROWSER == "chrome":
            options = Options()
            options.add_argument("--no-sandbox")
            cls.browser = TEST_DRIVER(chrome_options=options)
        else:
            cls.browser = TEST_DRIVER()

        # configure the window size
        (width, height) = SELENIUM_WINDOW_SIZE.lower().split("x")
        cls.browser.set_window_size(int(width), int(height))

        # An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find any element (or elements) not immediately available. The default setting is 0. Once set, the implicit wait is set for the life of the WebDriver object.
        # cls.browser.implicitly_wait(3)  # seconds

        # clear url cache
        clear_url_caches()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addCleanup(DebugTestMixin.render_footer_log, self)
        self.render_header_log()

    # Tear down the Selenium web browser
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()
