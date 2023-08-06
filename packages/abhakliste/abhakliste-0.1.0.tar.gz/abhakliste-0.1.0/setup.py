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
    'version': '0.1.0',
    'description': 'Running multiple assertion tests one after another.',
    'long_description': '# Abhakliste\n\nAbhakliste is a minimal task runner that prints a list of tasks and their status.\nIt runs a collection of dependent task which can be shell commands or python functions in sequence\nand checks for error. Even if one task fails, it continues to run the rest of the tasks.\nThe goal of this project is to provide a minimal task runner with a low overhead API.\n\n![Screenshot](./docs/assets/screenshot.png)\n\n## ⚙️ Installation\n\nInstall the project with `pip`\n\n```bash\npip install abhakliste\n```\n\n## 🎨 Features\n\n- Low Overhead Task Runner\n- Visual summary of task results\n- Written in pure python (no modules)\n- Supports Python 3.8+\n\n## 💡 Usage Examples\n\n```python\nimport subprocess\nfrom abhakliste import Abhakliste\n\n# set up runner\nabhaker = Abhakliste()\n\n# run code context\nwith abhaker.run_context(desc="Run ls"):\n  subprocess.check_output("ls")\n\n# run cli command\nabhaker.run_cmd("ls", desc="Run ls")\n\n# run function\ndef run_ls():\n  subprocess.check_output("ls")\nabhaker.run_func(run_ls, desc="Run ls")\n\n# raise an error if a run failed\nabhaker.raise_on_error()\n```\n',
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
