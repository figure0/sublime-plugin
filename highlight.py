import sublime
import sublime_plugin

from .persist import DB, HIGHLIGHTED_REGIONS
from .consts import HIGHLIGH_REGION_NAME


def get_highlight_color(severity):
    if severity == 1:
        return 'region.redish.plugin'
    elif severity == 2:
        return 'region.yellowish.plugin'
    else:
        return 'region.bluish.plugin'

def generate_unique_region_name(*args):
    return ''.join(list(map(str, args)))

def highlight_errors(view):
    if not view.window() or len(view.window().folders()) == 0:
        return


    project_path = view.window().folders()[0]
    project_errors = DB.get(project_path)
    if project_errors is None or view.file_name() is None:
        return

    file_name = view.file_name()
    errors_in_active_file = project_errors.get('files').get(file_name)
    suggestions = project_errors.get('suggestions')
    HIGHLIGHTED_REGIONS[file_name] = []
    print('____LOGER____')
    if errors_in_active_file:
        suggestions_for_file = list(errors_in_active_file.keys())
        for s, errors in errors_in_active_file.items():
            suggestion = suggestions.get(s)
            for error_data in errors:
                error_start_point = view.text_point(error_data.get('rows')[0] - 1, error_data.get('cols')[0])
                error_end_point = view.text_point(error_data.get('rows')[0] - 1, error_data.get('cols')[1])
                name = generate_unique_region_name(error_start_point, error_end_point, file_name)
                HIGHLIGHTED_REGIONS[file_name].append({ 'region': range(error_start_point, error_end_point + 1), 'message': suggestion.get('message'), 'name': name, 'severity': suggestion.get('severity'), 'id': suggestion.get('rule')})
                color = get_highlight_color(suggestion.get('severity'))
                view.add_regions(name, list(map(view.word, range(error_start_point, error_end_point + 1))), color, "", sublime.DRAW_SQUIGGLY_UNDERLINE|sublime.DRAW_NO_FILL|sublime.DRAW_NO_OUTLINE)

def clear_previous_highlight(view):
    if not view.window() or len(view.window().folders()) == 0:
        return

    project_path = view.window().folders()[0]
    for filename, file_regions in HIGHLIGHTED_REGIONS.items():
        if project_path in filename:
            for region in file_regions:
                view.erase_regions(region['name'])
            HIGHLIGHTED_REGIONS[filename] = []
