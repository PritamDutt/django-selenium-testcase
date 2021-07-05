from time import time, sleep

from django.conf import settings
from selenium.common.exceptions import WebDriverException

# Note: This function was adapted from code in the aloe-webdriver
# project (under the MIT license)
# https://github.com/aloetesting/aloe_webdriver
from selenium.webdriver.support.wait import WebDriverWait


def wait_for(func):
    """
    A decorator to invoke a function, retrying on assertion errors for a
    specified time interval.

    Adds a kwarg `timeout` to `func` which is a number of seconds to try
    for (default 15).
    """

    def wrapped(self, *args, **kwargs):

        # allow wait_for to be overridden by class or settings
        TIMEOUT = getattr(
            self, "selenium_timeout", getattr(settings, "SELENIUM_TESTCASE_TIMEOUT", 15)
        )

        # allow loop delay to be overridden by class or settings
        CHECK_EVERY = getattr(
            self,
            "selenium_check_every",
            getattr(settings, "SELENIUM_TESTCASE_CHECK_EVERY", 0.2),
        )

        # adjust timeout with a timeout=<integer seconds>
        timeout = kwargs.pop("timeout", TIMEOUT)

        start = None

        while True:
            try:
                # render the log file containing a screen shot on entry
                self.render_entry_log()
                # call the function
                return func(self, *args, **kwargs)
            except (AssertionError, WebDriverException) as e:
                # The function took some time to test the assertion, however,
                # the result might correspond to the state of the world at any
                # point in time, perhaps earlier than the timeout. Therefore,
                # start counting time from the first assertion fail, not from
                # before the function was called.
                if not start:
                    start = time()
                if time() - start < timeout:
                    sleep(CHECK_EVERY)
                    continue
                else:
                    # render exit template on error
                    self.render_exit_log()
                    raise e

    return wrapped


def wait_for_ajax(driver):
    wait = WebDriverWait(driver, 15)
    try:
        wait.until(lambda driver: driver.execute_script("return jQuery.active") == 0)
        wait.until(
            lambda driver: driver.execute_script("return document.readyState")
            == "complete"
        )
    except Exception as e:
        pass
