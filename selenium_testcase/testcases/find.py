from selenium.common.exceptions import NoSuchElementException

from ..settings import (
    PDB_ON_MISSING,
    TEXT_ON_MISSING,
    PNG_ON_MISSING,
)


class FindTestMixin:
    # exit to debugger on missing element
    pdb_on_missing = PDB_ON_MISSING

    # dump page text on missing element
    text_on_missing = TEXT_ON_MISSING

    # dump png image uri on missing element
    png_on_missing = PNG_ON_MISSING

    def _raise_no_such_element(self, message, *args, **kwargs):
        """ Raise missing exception with extra features. """

        if kwargs.get("text", self.text_on_missing):
            message += "---\n" + self.get_visible_text() + "\n---\n"

        # dump image data link to exception message
        if kwargs.get("png", self.png_on_missing):
            message += "---\n" + self.get_image_uri() + "\n---\n"

        # exit to pdb if flag is set
        if kwargs.get("pdb", self.pdb_on_missing):
            import pdb

            pdb.set_trace()

        # raise the exception if we get this far
        raise NoSuchElementException(message)

    def find_text(self, text, *args, **kwargs):
        """ Return true if text is found on page. """

        visible_text = self.get_visible_text()

        if text in visible_text:
            return True

        # if we get this far, raise exception
        message = "Unable to find {} on page:\n".format(text)
        self._raise_no_such_element(message, *args, **kwargs)

    def find_element(self, search_list, *args, **kwargs):
        """ Return a single element by optional index. """
        index = kwargs.get("index", 0)
        kwargs["count"] = index + 1
        elements = self.find_elements(search_list, *args, **kwargs)
        return elements[index]

    def find_elements(self, search_list, *args, **kwargs):
        """ Traverse a search list looking for count visible elements. """

        # find this many visible elements at a minimum
        count = kwargs.get("count", 1)

        # construct error message string just in case
        message = "Unable to find element, tried:\n"

        for method, pattern in search_list:

            # format the string as necessary
            # ignore index out of range values
            try:
                value = pattern.format(*args)
            except IndexError:
                continue

            # add method and value about to try
            message += "{}: {}\n".format(method, value)

            # try each of the patterns in order
            try:
                elements = self.browser.find_elements(method, value)
            except NoSuchElementException:
                pass
            else:
                # filter down to visible elements
                visible = [e for e in elements if e.is_displayed()]

                # try next if we don't have enough visible elements
                if len(visible) < count:
                    continue
                else:
                    return visible

        # raise the exception if we get this far
        self._raise_no_such_element(message, *args, **kwargs)
