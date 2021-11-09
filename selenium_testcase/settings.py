import os

from django.conf import settings
from selenium import webdriver

from .testcases import headless

# choose the test browser class from this list
BROWSER_CHOICES = {
    "chrome": webdriver.Chrome,
    "chrome-headless": headless.Chrome,
    "edge": webdriver.Edge,
    "firefox": webdriver.Firefox,
    "firefox-headless": headless.Firefox,
    "ie": webdriver.Ie,
    "opera": webdriver.Opera,
    "safari": webdriver.Safari,
}

# exit to debugger on missing element
PDB_ON_MISSING = os.getenv(
    "PDB_ON_MISSING", getattr(settings, "SELENIUM_TESTCASE_PDB_ON_MISSING", False)
)

# dump page text on missing element
TEXT_ON_MISSING = os.getenv(
    "TEXT_ON_MISSING", getattr(settings, "SELENIUM_TESTCASE_TEXT_ON_MISSING", False)
)

# dump png image uri on missing element
PNG_ON_MISSING = os.getenv(
    "PNG_ON_MISSING", getattr(settings, "SELENIUM_TESTCASE_PNG_ON_MISSING", False)
)

TEST_BROWSER = os.getenv(
    "TEST_BROWSER", getattr(settings, "SELENIUM_TEST_BROWSER", "chrome")
).lower()

TEST_DRIVER = BROWSER_CHOICES[TEST_BROWSER]

# selenium logging
SELENIUM_LOGGING = os.getenv(
    "SELENIUM_LOGGING", getattr(settings, "SELENIUM_TESTCASE_LOGGING", False)
)

# set the window size to 1024x768
SELENIUM_WINDOW_SIZE = os.getenv(
    "SELENIUM_WINDOW_SIZE", getattr(settings, "SELENIUM_WINDOW_SIZE", "1024x768")
)
