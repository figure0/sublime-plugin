# DeepCodeAI package for Sublime

**The Sublime package provided by <a href="https://www.deepcode.ai/">DeepCode.ai</a> finds bugs and critical vulnerabilities in your code. We support Java, Python, JavaScript, TypeScript and C/C++.**


# Table of Contents

1. DeepCode package - what is it?
2. Installation
   1. How to install the package
   2. Tips on project onboarding
3. How to use it?
   1. How to analyze project
   2. How to open results panel 
   3. How to ignore suggestions
   4. Rescan
   5. View results online
   6. Settings
4. Feedback and contact

# DeepCode package

Through the package you can quickly start using DeepCode's code review and analysis within your development workflow. The package will automatically alert you about critical vulnerabilities you need to solve in your code the moment when you hit Save in your IDE. With DeepCode's superior code review you save time finding and fixing bugs before they go to production.

## DeepCode's AI Engine finds bugs 

DeepCode uses symbolic AI to process hundreds of millions of commits in open sorce software projects and learns how to find serious coding issues. Because the platform determines the intent of the code — and not only the syntax mistakes — DeepCode identifies 10x more critical bugs and security vulnerabilities than other tools.

## Our AI provides explanation behind found bugs

In order to show detailed explanation why something was flagged as bug we introduced a new AI technique called Ontology. With Ontology, we’ve integrated the capability to present logical conclusions within the DeepCode engine.

## Supported languages

Python, JavaScript/TypeScript, Java, C/C++ are currently supported.

# Installation

## How to install the package
DeepCode Sublime plugin is available in install package menu 

#### Command Palette
   1.  Open the command palette
   2. Win/Linux: ctrl+shift+p, Mac: cmd+shift+p
   3. Type Install Package, press enter
   4. Type DeepCode Sublime Plugin, press enter
This will download the latest version of DeepCode Sublime Plugin,  and it will install package and his dependencies on your machine.

## Tips on project onboarding

- we are serious when it comes to your code. We upload and analyse your code only after you giving us the consent to do so. Your code is protected and used only for the purpose of
informing you about issues in code:

   ![confirm](images/consent.png)

- once the confirmation is in place we start uploading the files:

   ![deepcode progress](images/progress.png)

# How to use it?

## Scan or Rescan from context menu

- Analysis will run on command by selecting `Analyze Project` from `DeepCode` context menu option.
 ![deepcode analyze](images/ctx_analyze.png)
 
## Analysis on Save

- Analysis will run on file save event, so you don't have to worry about rescanning project manually.

## How to ignore suggestions

There are two key steps here:

   1. Ignore particular alert directly by using `Ignore for line` or `Ignore for file`:
 
      ![deepcode problem](images/problem.png)

   2. DeepCode will create a comment, that will inform our analysis engine to ignore it. Don't forget to specify a description why you think it needs to be ignored. Your feedback will improve our engine over time:

## Opening Results Panel  
  
There are two ways to open *Results Panel*

   1. Open Results Panel from context menu. 
   ![deepcode open results](images/results panel_ctx.png)
  
   2. Open Results Panel from panel menu
   ![deepcode open results](images/open_results.png)
   
## Results Panel 

  Results panel is a place where you can check analysis results grouped by the file.
  ![deepcode panel](images/panel.png)
  
 ####  Actions from Results Panel:
   1. See Results In Dashboard (opens your analysis results in your default browser where you can also see example fixes)
   2. Ignore for Line and Ignore for file (adds ignore comment)
   3. Go to File (focuses the line with the issue in the specific file) 

## Settings
   
   You can customize behavior of the package by adding your custom settings in `Settings` section, which you can open either form context menu or from Preferences menu
   ![configuration](images/settings_menu.png)
   
  If you need to update the url to the DeepCode server in a self-managed environment or restart the login process, or remove your project form consented list just modify the settings file.
   ![settings](images/settings.png)

# Feedback and contact

- In case you need to contact us or provide feedback, we would love to hear from you - [here is how to get in touch with us](https://www.deepcode.ai/feedback).
- If you need to update this file, you can do so by [editing this README.md](https://github.com/DeepCodeAI/sublime-plugin/edit/master/README.md).
