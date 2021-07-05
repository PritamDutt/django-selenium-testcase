from selenium.common.exceptions import NoSuchElementException

from .utils import wait_for


class ContentTestMixin:
    def should_see_immediately(self, text, **kwargs):
        """ Assert that DOM contains the given text. """
        return self.find_text(text, **kwargs)

    @wait_for
    def should_see(self, text, **kwargs):
        """ Wait for text to appear before testing assertion. """
        return self.should_see_immediately(text, **kwargs)

    def should_not_see(self, text, **kwargs):
        """ Wait for text to not appear before testing assertion. """
        self.assertRaises(NoSuchElementException, self.should_see, text, **kwargs)

    @wait_for
    def title_should_be(self, title, **kwargs):
        """ Assert that page title matches. """
        self.assertEqual(self.browser.title, title)

    def title_should_not_be(self, title, **kwargs):
        """ Assert when page title does not match. """
        self.assertRaises(AssertionError, self.title_should_be, title, **kwargs)

    @wait_for
    def title_should_contain(self, text, **kwargs):
        """ Assert that page title contains text. """
        self.assertIn(text, self.browser.title)

    def title_should_not_contain(self, text, **kwargs):
        """ Assert that page title does not contain text. """
        self.assertRaises(AssertionError, self.title_should_contain, text, **kwargs)

    @wait_for
    def source_should_contain(self, text, **kwargs):
        """ Assert that page source contains text. """
        self.assertIn(text, self.browser.page_source)

    def source_should_not_contain(self, text, **kwargs):
        """ Assert that page source does not contain text. """
        self.assertRaises(AssertionError, self.source_should_contain, text, **kwargs)
