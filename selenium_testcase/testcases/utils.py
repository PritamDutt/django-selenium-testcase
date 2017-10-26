# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sys

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


# Note: This function was adapted from
# http://codeinthehole.com/tips/how-to-reload-djangos-url-config/

def reload_urlconf(urlconf=None):
    if urlconf is None:
        urlconf = settings.ROOT_URLCONF
    if urlconf in sys.modules:
        reload(sys.modules[urlconf])
