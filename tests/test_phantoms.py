import unittest, sublime

from DeepcodeAI.phantoms import add_see_results_phantom


class TestPhantoms(unittest.TestCase):
    def setUp(self):
        # do something before running the test suite
        print(sublime.active_window())
        pass

    def test_1(self):
        panel = sublime.active_window().create_output_panel("test_1")
        add_see_results_phantom(panel, "http://test-link.com")
        panel.find("See Results In Dashboard", 0, sublime.IGNORECASE)
        self.assertIsNone(panel.erase_phantoms("see_results"))


if __name__ == "__main__":
    unittest.main()
