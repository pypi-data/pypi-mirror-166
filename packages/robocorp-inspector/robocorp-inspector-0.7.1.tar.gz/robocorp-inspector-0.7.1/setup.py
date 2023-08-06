# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['inspector', 'inspector.windows']

package_data = \
{'': ['*'],
 'inspector': ['static/*', 'static/assets/fonts/*', 'static/resources/*']}

install_requires = \
['mss>=6.1.0,<7.0.0',
 'pynput-robocorp-fork>=4.0.0,<5.0.0',
 'pywebview==3.6.3',
 'requests>=2.25.1,<3.0.0',
 'rpaframework-core>=7.0.1,<8.0.0',
 'rpaframework-recognition>=2.0.0,<3.0.0',
 'typing-extensions>=3.10.0,<4.0.0',
 'uiautomation>=2.0.16,<3.0.0']

extras_require = \
{':python_full_version < "3.7.6" and sys_platform == "win32" or python_full_version > "3.7.6" and python_full_version < "3.8.1" and sys_platform == "win32" or python_full_version > "3.8.1" and sys_platform == "win32"': ['pywin32>=302,<304'],
 ':sys_platform == "darwin"': ['pyobjc-core>=7.3,<8.0',
                               'pyobjc-framework-cocoa>=7.3,<8.0',
                               'pyobjc-framework-quartz>=7.3,<8.0',
                               'pyobjc-framework-webkit>=7.3,<8.0']}

entry_points = \
{'console_scripts': ['inspector = inspector.cli:run']}

setup_kwargs = {
    'name': 'robocorp-inspector',
    'version': '0.7.1',
    'description': 'Robocorp Inspector',
    'long_description': '# Robocorp Inspector\n\nRobocorp Inspector is a tool for exploring various user interfaces\nand developing ways to target elements within them. An expression\nthat can target specific UI elemements is called a _locator_, and\nthese locators can be used to automate applications typically\nused by humans.\n\n## Development\n\nThe project uses `invoke` for overall project management, `poetry` for\npython dependencies and environments, and `yarn` for Javascript dependencies\nand building.\n\nBoth `invoke` and `poetry` should be installed via pip: `pip install poetry invoke`\n\n- To see all possible tasks: `invoke --list`\n- To run the project: `invoke run `\n\nAll source code is hosted on [GitHub](https://github.com/robocorp/inspector/).\n\n## Usage\n\nRobocorp Inspector is distributed as a Python package with all front-end\ncomponents compiled and included statically.\n\nIf the package (and all required dependencies) is installed manually,\nit can be run with the command: `inspector`.\n\n---\n\n<p align="center">\n  <img height="100" src="https://cdn.robocorp.com/brand/Logo/Dark%20logo%20transparent%20with%20buffer%20space/Dark%20logo%20transparent%20with%20buffer%20space.svg">\n</p>\n',
    'author': 'Ossi Rajuvaara',
    'author_email': 'ossi@rajuvaara.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/robocorp/inspector',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
