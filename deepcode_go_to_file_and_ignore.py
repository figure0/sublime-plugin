import sublime
import sublime_plugin


class DeepcodeGoToFileAndIgnoreCommand(sublime_plugin.TextCommand):
    def open_file_and_add_deepcode_ignore_comment(self, view, file, row, col, type, reason):
        view.run_command('deep_code_ignore', {'point': view.text_point(row - 1, col), 'type': type,'id': reason})
        sublime.set_timeout_async(view.show_at_center(view.text_point(row - 1, col)), 500)

    def run(self, edit, file, row, col, type, reason):
        view = self.view.window().open_file(file);
        sublime.set_timeout_async(lambda: self.open_file_and_add_deepcode_ignore_comment(view, file, row, col, type, reason), 500)
