from .consts import ERROR, WARNING

def get_color_for_severity(severity):
    if severity is WARNING:
        return '⚠️'
    elif severity is ERROR:
        return '⛔'
    else:
        return ' ⓘ'

def get_popup_content(message, severity):
	return """
	  <div style="display: block; height: auto; overflow-y: visible; padding: 10px 0; height: auto">
      <span>{}</span>
      <span>{}</span>

       <div style="display: block; padding: 20px 25px 0">
          <a href="line" style="text-decoration: none; border: 1px solid lightgray; width: 160px; text-align: center; padding: 4px 20px; color: lightgray; font-size: 10px; border-radius: 5px;">Ignore for line</a>
          <a href="file" style="text-decoration: none; border: 1px solid lightgray; width: 160px; text-align: center; padding: 4px 20px; color: lightgray; font-size: 10px; border-radius: 5px;">Ignore for file</a>
        </div>

         <div style="display: block; padding: 20px 25px 0">
          <a href="panel" style="text-decoration: none; width: 260px; text-align: center; cursor: pointer; color: lightblue; font-size: 10px; border-radius: 5px;">Show all problems...</a>
        </div>
    </div> 
  """.format(get_color_for_severity(severity), message)