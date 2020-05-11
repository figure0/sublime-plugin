import unittest

from deepcode_sublime.consts import ERROR, WARNING, INFO
from deepcode_sublime.popup import get_color_for_severity


class TestUtils(unittest.TestCase):
    def setUp(self):
        # do something before running the test suite
        pass

    def test_get_error_icon(self):
        icon = get_color_for_severity(ERROR)
        self.assertEqual(icon, "⛔")

    def test_get_warning_icon(self):
        icon = get_color_for_severity(WARNING)
        self.assertEqual(icon, "⚠️")

    def test_get_info_icon(self):
        icon = get_color_for_severity(INFO)
        self.assertEqual(icon, " ⓘ")


if __name__ == "__main__":
    unittest.main()
