import os
import sublime
import unittest

from ..consts import INFO, WARNING, ERROR
from ..utils import (
    find,
    is_global_python_version_compatible,
    merge_two_lists,
    get_severity_status_string,
    get_error_count,
)


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.real_path_environ = os.environ["PATH"]
        self.subl_error_message = sublime.error_message
        self.message_info = {}
        self.message_info[INFO] = 11
        self.message_info[WARNING] = 7
        self.message_info[ERROR] = 4

    def test_find_success(self):
        errors = [
            {"id": 1, "region": range(123, 222)},
            {"id": 2, "region": range(389, 562)},
        ]
        point = 437
        elem = find(point, errors)
        self.assertEqual(elem.get("id"), 2)

    def test_find_failure(self):
        errors = [
            {"id": 1, "region": range(123, 222)},
            {"id": 2, "region": range(389, 562)},
        ]
        point = 837
        elem = find(point, errors)
        self.assertRaises(Exception)

    def test_is_global_python_version_compatible_success(self):
        return_val = is_global_python_version_compatible()
        self.assertEqual(return_val, True)

    def test_is_global_python_version_compatible_fail(self):
        os.environ["PATH"] = os.path.sep
        sublime.error_message = print
        return_val = is_global_python_version_compatible()
        self.assertEqual(return_val, False)
        os.environ["PATH"] = self.real_path_environ
        sublime.error_message = self.subl_error_message

    def test_merge_two_lists_both_empty(self):
        result = merge_two_lists([], [])
        self.assertEqual(len(result), 0)

    def test_merge_two_lists_one_empty(self):
        result = merge_two_lists(["one", "two", 3], [])
        self.assertEqual(len(result), 3)
        self.assertIn("one", result)

    def test_merge_two_lists_both_with_elements(self):
        result = merge_two_lists(["one", "two", 3], ["blue", True, "something"])
        self.assertEqual(len(result), 6)
        self.assertIn("one", result)
        self.assertIn("something", result)
        self.assertIn(True, result)

    def test_merge_two_lists_with_overlapping_elements(self):
        result = merge_two_lists(["one", "two", 3, True], ["blue", True, "one"])
        self.assertEqual(len(result), 5)
        self.assertIn("one", result)
        self.assertIn("blue", result)
        self.assertIn(True, result)

    def test_get_severity_status_string_info(self):
        result = get_severity_status_string(INFO)
        self.assertEqual(result, "   ⓘ")

    def test_get_severity_status_string_warning(self):
        result = get_severity_status_string(WARNING)
        self.assertEqual(result, "   ⚠️")

    def test_get_severity_status_string_error(self):
        result = get_severity_status_string(ERROR)
        self.assertEqual(result, "   ⛔")

    def test_get_error_count(self):
        result = get_error_count(self.message_info, "something something ")
        self.assertEqual(result, "something something ⛔ 4 ⚠️ 7 ⓘ 11 ")


if __name__ == "__main__":
    unittest.main()
