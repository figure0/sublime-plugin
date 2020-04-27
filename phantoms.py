import sublime
from .consts import PANEL_IGNORE_PHANTOM_BASE_NAME

def parse_link_data_and_ignore(view, link):
    link_list = link.split('☡')
    print(link_list)
    view.window().run_command("deepcode_go_to_file_and_ignore", {"file": link_list[1], "type": link_list[0], "row": int(link_list[2]), "col": int(link_list[3]), "reason": link_list[4]})

def add_ingore_commands_phantom(panel, phantom_counter, file_name, issue):
    sublime.set_timeout_async(lambda: panel.add_phantom(
        '{}-{}'.format(PANEL_IGNORE_PHANTOM_BASE_NAME, phantom_counter),
        panel.line(panel.find(issue['message'][8:], 0, sublime.LITERAL)),
        '''
        <div style="margin: 0.5em 0 30px 8em">
          <a href="line☡{}☡{}☡{}☡{}" style="font-weight: bold; color: lightgray; font-size: 0.8em; text-decoration: none; padding: 5px 20px; border-top: 10px solid gray; border: 1px solid gray; border-radius: 5px">Ignore For Line</a>
          <a href="file☡{}☡{}☡{}☡{}" style="font-weight: bold; color: lightgray; font-size: 0.8em; text-decoration: none; padding: 5px 20px; border-top: 10px solid gray; border: 1px solid gray; border-radius: 5px">Ignore For File</a>
        </div>
        '''.format(file_name, issue['row'], issue['col'], issue['reason'], file_name, issue['row'], issue['col'], issue['reason']),
        sublime.LAYOUT_BELOW,
        lambda x: parse_link_data_and_ignore(panel, x)
    ))
	

 
def add_see_results_phantom(panel, link):
    panel.erase_phantoms('see_results')
    sublime.set_timeout_async(lambda: panel.add_phantom(
        'see_results',
        panel.find('›', 0, sublime.IGNORECASE),
        '<a href="{}" style="font-weight: bold; color: #fff; font-size: 13px;">See Results In Dashboard</a>'.format(link),
        sublime.LAYOUT_INLINE,
        lambda x: panel.window().run_command ("open_url", {"url": x})
    ), 100)

def remove_previous_phantoms(panel, phantom_counter):
    for phantom_index in range(phantom_counter + 1):
        panel.erase_phantoms('{}-{}'.format(PANEL_IGNORE_PHANTOM_BASE_NAME, phantom_index))
    phantom_counter = 0


def add_settings_key_description_phantom(view, settings_key, description):
    sublime.set_timeout_async(lambda: view.add_phantom(
        view.name(),
        view.find(settings_key, 0, sublime.IGNORECASE),
        '<p style="font-size: 12px; color: lightgray; padding: 0; margin: 0">Settings Option - <b style="font-size: 13px; color: snow">{}</b>:</p><p style=" padding: 0; margin: 0 0 20px 0; color: lightblue; font-size: 11px;">{}</p>'.format(settings_key, description),
        sublime.LAYOUT_BELOW,
        lambda x: print(x)
    ))