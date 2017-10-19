# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

from selenium.common.exceptions import StaleElementReferenceException
from time import time, sleep

from django.conf import settings

# allow wait_for to be overridden by settings
TIMEOUT = getattr(settings, 'SELENIUM_TESTCASE_TIMEOUT', 15)
CHECK_EVERY = getattr(settings, 'SELENIUM_TESTCASE_CHECK_EVERY', 0.2)


# Note: This function was copied from code in the aloe-webdriver
# project (under the MIT license)
# https://github.com/aloetesting/aloe_webdriver

def wait_for(func):
    """
    A decorator to invoke a function, retrying on assertion errors for a
    specified time interval.

    Adds a kwarg `timeout` to `func` which is a number of seconds to try
    for (default 15).
    """

    def wrapped(*args, **kwargs):
        timeout = kwargs.pop('timeout', TIMEOUT)

        start = None

        while True:
            try:
                return func(*args, **kwargs)
            except AssertionError:
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
                    raise

    return wrapped


# Note: This function was copied from code in the aloe-webdriver
# project (under the MIT license)
# https://github.com/aloetesting/aloe_webdriver

def string_literal(content):
    """
    Choose a string literal that can wrap our string.

    If your string contains a ``\'`` the result will be wrapped in ``\"``.
    If your string contains a ``\"`` the result will be wrapped in ``\'``.

    Cannot currently handle strings which contain both ``\"`` and ``\'``.
    """

    if '"' in content and "'" in content:
        # there is no way to escape string literal characters in XPath
        raise ValueError("Cannot represent this string in XPath")
    elif '"' in content:  # if it contains " wrap it in '
        content = "'%s'" % content
    else:  # wrap it in "
        content = '"%s"' % content

    return content


# Note: This function was adapted from code in the aloe-webdriver
# project (under the MIT license)
# https://github.com/aloetesting/aloe_webdriver

def dom_contains(browser, content):
    """
    Search for an element that contains the whole of the text we're looking
    for in it or its subelements, but whose children do NOT contain that
    text - otherwise matches <body> or <html> or other similarly useless
    things.
    """
    for elem in browser.find_elements_by_xpath(str(
            '//*[contains(normalize-space(.), {content}) '
            'and not(./*[contains(normalize-space(.), {content})])]'
            .format(content=string_literal(content)))):

        try:
            if elem.is_displayed():
                return True
        except StaleElementReferenceException:
            pass

    return False


# Note: This function was adapted from
# http://codeinthehole.com/tips/how-to-reload-djangos-url-config/

def reload_urlconf(urlconf=None):
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
