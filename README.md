django-selenium-testcase
========================

[![pipeline status](https://gitlab.nimbis.io/nimbis/sites/django-selenium-testcase/badges/master/pipeline.svg)](https://gitlab.nimbis.io/nimbis/sites/django-selenium-testcase/-/commits/master)

[![coverage report](https://gitlab.nimbis.io/nimbis/sites/django-selenium-testcase/badges/master/coverage.svg)](https://gitlab.nimbis.io/nimbis/sites/django-selenium-testcase/-/commits/master)

This repository implements a simple subclass of Django LiveServerTestCase that
enables selenium testing of the Django live server.  Rather than relying on
Gherkin syntax found in Lettuce and Aloe tools, this package favors of python
function calls and method decorators directly available in the TestCase
namespace.

Integration testing is never easy and we found that adding a layer of regular
expression parsing and a separate test runner system moved code complexity from
the application to the test fixtures.  This module gives us an easy way to get
similar aloe/lettuce functionality of interface testing without having to build
separate test fixtures.

Quick Start
-----------

- Add 'selenium_testcase' to INSTALLED_APPS.
- Add "url(r'', include('selenium_testcase.urls'))" to urls.py.
- Use the SeleniumLiveTestCase instead of LiveServerTestCase.

```
# -*- coding: utf-8 -*-


from selenium_testcase.testcases import SeleniumLiveTestCase


class HomepageTestCase(SeleniumLiveTestCase):

    test_templates = [(r'', 'test.html')]

    def test_homepage(self):
        """
        Test that the home page has expected title and content.
        """
        self.get_page("/")
        self.should_see("This is a test.")
        self.title_should_be("Test")
```

History
-------
See file CHANGES
