from .consts import ERROR, WARNING
from Default.comment import build_comment_data


def get_color_for_severity(severity):
    if severity is WARNING:
        return "⚠️"
    elif severity is ERROR:
        return "⛔"
    else:
        return " ⓘ"


def get_popup_action(link, label, is_disabled=True):
    color = "gray" if is_disabled else "lightgray"
    return """
  <a href="{}" style="text-decoration: none; border: 1px solid {}; width: 160px; text-align: center; padding: 4px 20px; color: {}; font-size: 10px; border-radius: 5px;">{}</a>
  """.format(
        link, color, color, label
    )


def get_popup_actions(view):
    data = build_comment_data(view, view.size())
    comment_message = ""

    if not data[0] and not data[1]:
        comment_message = '<p style="font-size: 10px; color: #FFBF00; margin: 0 0 10px 0; padding: 0">ⓘ You must select/install proper syntax in order to add ignore comments.</p>'

    return """
    <div style="display: block; padding: 20px 25px 0">
      {}
      {}
      {}
    </div>

    """.format(
        comment_message,
        get_popup_action("line", "Ignore for line", bool(comment_message)),
        get_popup_action("file", "Ignore for file", bool(comment_message)),
    )


def get_popup_content(message, severity, view):

    return """
	  <div style="display: block; height: auto; overflow-y: visible; padding: 10px 0; height: auto">
      <span>{}</span>
      <span>{}</span>
      {}

       <div style="display: block; padding: 20px 25px 0">
        <a href="panel" style="text-decoration: none; width: 260px; text-align: center; cursor: pointer; color: lightblue; font-size: 10px; border-radius: 5px;">Show all problems...</a>
      </div>
    </div> 
    """.format(
        get_color_for_severity(severity), message, get_popup_actions(view)
    )
