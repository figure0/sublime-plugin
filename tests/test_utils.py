import unittest
from unittest.mock import patch

from deepcode_sublime_plugin.utils import find


class TestUtils(unittest.TestCase):
    def setUp(self):
        # do something before running the test suite
        pass

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


if __name__ == "__main__":
    unittest.main()
