# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cursesmenu', 'cursesmenu.items']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2.13,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.7.0'],
 ':sys_platform == "win32"': ['windows-curses==2.3.0']}

setup_kwargs = {
    'name': 'curses-menu',
    'version': '0.6.6',
    'description': 'A simple console menu system using curses',
    'long_description': '|Build Status|\\ |Documentation Status|\\ |Coverage Status|\n\ncurses-menu\n===========\n\nA simple Python menu-based GUI system on the terminal using curses.\nPerfect for those times when you need a GUI, but don’t want the overhead\nor learning curve of a full-fledged GUI framework. However, it\'s also\nflexible enough to do cool stuff like on-the-fly changing of menus and is extensible to\na large variety of uses.\n\nhttp://curses-menu.readthedocs.org/en/latest/\n\n.. image:: ./images/curses-menu_screenshot1.png\n\n\nInstallation\n~~~~~~~~~~~~\n\nTested on Python 3.7+ pypy and pypy3.\n\nThe curses library comes bundled with python on Linux and MacOS. Windows\nusers can visit http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses and\nget a third-party build for your platform and Python version.\n\nThen just run\n\n.. code:: shell\n\n   pip install curses-menu\n\nUsage\n-----\n\nIt’s designed to be pretty simple to use. Here’s an example\n\n.. code:: python\n\n    # Import the necessary packages\n    from cursesmenu import *\n    from cursesmenu.items import *\n\n    # Create the menu\n    menu = CursesMenu("Title", "Subtitle")\n\n    # Create some items\n\n    # MenuItem is the base class for all items, it doesn\'t do anything when selected\n    menu_item = MenuItem("Menu Item")\n\n    # A FunctionItem runs a Python function when selected\n    function_item = FunctionItem("Call a Python function", input, ["Enter an input"])\n\n    # A CommandItem runs a console command\n    command_item = CommandItem("Run a console command", "touch hello.txt")\n\n    # A SelectionMenu constructs a menu from a list of strings\n    selection_menu = SelectionMenu(["item1", "item2", "item3"])\n\n    # A SubmenuItem lets you add a menu (the selection_menu above, for example)\n    # as a submenu of another menu\n    submenu_item = SubmenuItem("Submenu item", selection_menu, menu)\n\n    # Once we\'re done creating them, we just add the items to the menu\n    menu.items.append(menu_item)\n    menu.items.append(function_item)\n    menu.items.append(command_item)\n    menu.items.append(submenu_item)\n\n    # Finally, we call show to show the menu and allow the user to interact\n    menu.show()\n\nTesting Information\n-------------------\n\nCurrently the platforms I\'m manually testing on are MacOS in iTerm2 on zsh with and without TMUX and Windows 10\\\nwith both powersehll and cmd.exe in and out of Windows Terminal. If a bug pops up on another configuration, \\\nno promises that I\'ll be able to reproduce it.\n\n.. |Build Status| image:: https://github.com/pmbarrett314/curses-menu/actions/workflows/github-action-tox.yml/badge.svg\n   :target: https://github.com/pmbarrett314/curses-menu/actions/workflows/github-action-tox.yml/badge.svg\n.. |Documentation Status| image:: https://readthedocs.org/projects/curses-menu/badge/?version=latest\n   :target: http://curses-menu.readthedocs.org/en/latest/?badge=latest\n.. |Coverage Status| image:: https://coveralls.io/repos/github/pmbarrett314/curses-menu/badge.svg?branch=develop\n   :target: https://coveralls.io/github/pmbarrett314/curses-menu?branch=develop\n',
    'author': 'Paul Barrett',
    'author_email': 'pmbarrett314@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://github.com/pmbarrett314/curses-menu',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
