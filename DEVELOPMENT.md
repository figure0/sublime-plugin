# Deepcode Sublime Instructions

## Requirements

#### Minimal supported systems python version is: 3.6.5 

## Steps

1. Install Sublime Text 3
2. Open Sublime Text and install Package Control (https://packagecontrol.io/installation)
3. Go to browse packages 
4. Create a directly (if not exists) 'DeepCodeAI'
5. Paste this folder's content into DeepCodeAI directory
5. Restart Sublime 
6. Go to List Installed Packages and check if DeepCodeAI is there
7. Go to DeepCodeAI and save file.


## Commands and Development

All plugin commands are prefixed with `deepcode_*.py`, and all of the util files are without prefix. 

For development after initial load, comment out  `patch_local_deepcode()` , so you dont have to wait for upgrade on each plugin reload.

    def plugin_loaded():
        ...
        patch_local_deepcode()
        ...

### List of commands (helper plugins)

1. **deepcode_analyze.py** - The command that starts the project analysis process, checks for auth status, has user consent
2. **deepcode_highlight.py** - The command in charge of highlighting regions, and showing the action pop-ups
3. **deepcode_ignore.py** - The command that is responsible for adding ignore the comment.
4. **deepcode_show_results_panel.py** - The command that opens analysis results panel (created after *deepcode_analyze* comand result)
5. **deepcode_settings.py** - The command that is responsible for validating user settings, and the look of general settings
6. **deepcode_open_results.py**  - The command in charge of of opening user default browser and navigating to specific url
7. **deepcode_go_to_file_and_ignore.py** - The command that opens specific file, and adds ignore comment to specific line by calling *deepcode_ignore* command


### Sublime Menus
1. **Main.sublime-menu** - defines content of plugins menu. (Preferences -> Package Settings -> Deepcode)
2. **Context.sublime-menu** - defines content and actions of context menu item (Deepcode)

### Plugin Settings
**DeepCodeAI.sublime-settings**
Default Plugin settings - **by default read-only** if you wish to change default settings file you must go to `deepcode_settings` command remove or comment out `view.set_read_only(True)` line.

#### Important note
When you change something in files, **you must reload commands that are affected by change**, and also main package command **DeepCodeAI.py**

Sometimes reload of sublime is needed, since plugin development environment is not that great. 

## Tests
 
Tests are located i *tests* directory, and they are bound to sublime environment, and therefor they must be run inside of sublime.

#### Instructions:

 1. Install ***Unit Testting*** plugin
 2. Run ***Unit Testting Command*** *(cmd + shift + p and type Unit Testing)*
 3. Enter plugin name in the input panel  *(DeepCodeAI)*
