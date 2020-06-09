import time
import unittest
from unittest.mock import patch

from ..deepcode_ignore import get_ignore_text, does_comment_exist, update_highlighted_region

class CustomDict(dict):
    pass

test_region = CustomDict({'file.py': [{
    'name': 'file.py',
    'id': 'replace~read~decode~json.loads',
    'message': 'Use decode before passing to json.loads.',
    'region': range(2925, 2935),
    'severity': 1
}]})
test_region.file_name = lambda: 'file.py'
test_region.rowcol = lambda x: (99, 22) if x == 2925 else (99, 31)
test_region.text_point = lambda _, x: 3027 if x == 22 else 3036

class TestUtils(unittest.TestCase):
    def setUp(self):
        self.test_string = "replace~read~decode~json.loads"
        self.test_region = test_region

    def test_get_ignore_text_for_line_new(self):
        text = get_ignore_text("line", self.test_string)
        expected_result = "deepcode ignore replace~read~decode~json.loads: <please specify a reason of ignoring this> \n"
        self.assertEqual(text, expected_result)

    def test_get_ignore_text_for_line_append(self):
        text = get_ignore_text("line", self.test_string, append=True)
        expected_result = ", deepcode ignore replace~read~decode~json.loads: <please specify a reason of ignoring this> \n"
        self.assertEqual(text, expected_result)

    def test_get_ignore_text_for_file_new(self):
        text = get_ignore_text("file", self.test_string)
        expected_result = "file deepcode ignore replace~read~decode~json.loads: <please specify a reason of ignoring this> \n"
        self.assertEqual(text, expected_result)

    def test_get_ignore_text_for_file_append(self):
        text = get_ignore_text("file", self.test_string, append=True)
        expected_result = ", file deepcode ignore replace~read~decode~json.loads: <please specify a reason of ignoring this> \n"
        self.assertEqual(text, expected_result)

    def test_does_comment_exist_true(self):
        exists = does_comment_exist(" deepcode ignore")
        self.assertTrue(exists)

    def test_does_comment_exist_false(self):
        exists = does_comment_exist("something else")
        self.assertFalse(exists)

    @patch.dict("DeepcodeAI.persist.HIGHLIGHTED_REGIONS", test_region)
    def test_update_highlighted_region(self):
        fake_text_point = 2933
        update_highlighted_region(self.test_region, fake_text_point)
        time.sleep(1)
        self.assertEqual(self.test_region['file.py'][0]['region'], range(3027, 3036))


if __name__ == "__main__":
    unittest.main()
