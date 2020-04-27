import unittest
from unittest.mock import patch

from deepcode_sublime_plugin.popup import get_color_for_severity


class TestUtils(unittest.TestCase):
    def setUp(self):
        # do something before running the test suite
        pass

    def test_get_error_icon(self):
        icon = get_color_for_severity(1)
        self.assertEqual(icon, '⛔')

    def test_get_warning_icon(self):
        icon = get_color_for_severity(2)
        self.assertEqual(icon, '⚠️')

    def test_get_info_icon(self):
        icon = get_color_for_severity(3)
        self.assertEqual(icon, ' ⓘ')

if __name__ == '__main__':
    unittest.main()