# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['abhakliste']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'abhakliste',
    'version': '0.1.1',
    'description': 'Running multiple assertion tests one after another.',
    'long_description': '# Abhakliste\n\n[![PyPI version](https://badge.fury.io/py/nbenumerate.svg)](https://badge.fury.io/py/nbenumerate)\n[![Python version](https://img.shields.io/badge/python-≥3.8-blue.svg)](https://pypi.org/project/kedro/)\n[![Publish Package](https://github.com/AnH0ang/abhakliste/actions/workflows/publish.yml/badge.svg)](https://github.com/AnH0ang/abhakliste/actions/workflows/publish.yml)\n[![Test](https://github.com/AnH0ang/abhakliste/actions/workflows/test.yml/badge.svg)](https://github.com/AnH0ang/abhakliste/actions/workflows/test.yml)\n[![Deploy to GitHub Pages](https://github.com/AnH0ang/abhakliste/actions/workflows/pages.yml/badge.svg)](https://github.com/AnH0ang/abhakliste/actions/workflows/pages.yml)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/STATWORX/statworx-theme/blob/master/LICENSE)\n![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)\n[![codecov](https://codecov.io/gh/AnH0ang/abhakliste/branch/master/graph/badge.svg?token=05CFXPPBPH)](https://codecov.io/gh/AnH0ang/abhakliste)\n\nAbhakliste is a minimal task runner that prints a list of tasks and their status.\nIt runs a collection of dependent task which can be shell commands or python functions in sequence\nand checks for error. Even if one task fails, it continues to run the rest of the tasks.\nThe goal of this project is to provide a minimal task runner with a low overhead API.\n\n![Screenshot](./docs/assets/screenshot.png)\n\n## ⚙️ Installation\n\nInstall the project with `pip`\n\n```bash\npip install abhakliste\n```\n\n## 🎨 Features\n\n- Low Overhead Task Runner\n- Visual summary of task results\n- Written in pure python (no modules)\n- Supports Python 3.8+\n\n## 💡 Usage Examples\n\n```python\nimport subprocess\nfrom abhakliste import Abhakliste\n\n# set up runner\nabhaker = Abhakliste()\n\n# run code context\nwith abhaker.run_context(desc="Run ls"):\n  subprocess.check_output("ls")\n\n# run cli command\nabhaker.run_cmd("ls", desc="Run ls")\n\n# run function\ndef run_ls():\n  subprocess.check_output("ls")\nabhaker.run_func(run_ls, desc="Run ls")\n\n# raise an error if a run failed\nabhaker.raise_on_error()\n```\n\n## 📜 Documentation\n\nFor further examples on how to use the modules and a detailed API reference, see the [documentation](https://anh0ang.github.io/abhakliste/).\n',
    'author': 'An Hoang',
    'author_email': 'anhoang31415@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
