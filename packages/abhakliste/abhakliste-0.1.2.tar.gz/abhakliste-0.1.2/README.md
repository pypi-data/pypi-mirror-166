# Abhakliste

[![PyPI version](https://badge.fury.io/py/nbenumerate.svg)](https://badge.fury.io/py/nbenumerate)
[![Python version](https://img.shields.io/badge/python-≥3.8-blue.svg)](https://pypi.org/project/kedro/)
[![Publish Package](https://github.com/AnH0ang/abhakliste/actions/workflows/publish.yml/badge.svg)](https://github.com/AnH0ang/abhakliste/actions/workflows/publish.yml)
[![Test](https://github.com/AnH0ang/abhakliste/actions/workflows/test.yml/badge.svg)](https://github.com/AnH0ang/abhakliste/actions/workflows/test.yml)
[![Deploy to GitHub Pages](https://github.com/AnH0ang/abhakliste/actions/workflows/pages.yml/badge.svg)](https://github.com/AnH0ang/abhakliste/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/STATWORX/statworx-theme/blob/master/LICENSE)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
[![codecov](https://codecov.io/gh/AnH0ang/abhakliste/branch/master/graph/badge.svg?token=05CFXPPBPH)](https://codecov.io/gh/AnH0ang/abhakliste)

Abhakliste is a minimal task runner that prints a list of tasks and their status.
It runs a collection of dependent task which can be shell commands or python functions in sequence
and checks for error. Even if one task fails, it continues to run the rest of the tasks.
The goal of this project is to provide a minimal task runner with a low overhead API.

![Screenshot](./docs/assets/screenshot.png)

## ⚙️ Installation

Install the project with `pip`

```bash
pip install abhakliste
```

## 🎨 Features

- Low Overhead Task Runner
- Visual summary of task results
- Written in pure python (no modules)
- Supports Python 3.8+

## 💡 Usage Examples

```python
import subprocess
from abhakliste import Abhakliste

# set up runner
abhaker = Abhakliste()

# run code context
with abhaker.run_context(desc="Run ls"):
  subprocess.check_output("ls")

# run cli command
abhaker.run_cmd("ls", desc="Run ls")

# run function
def run_ls():
  subprocess.check_output("ls")
abhaker.run_func(run_ls, desc="Run ls")

# raise an error if a run failed
abhaker.raise_on_error()
```

## 📜 Documentation

For further examples on how to use the modules and a detailed API reference, see the [documentation](https://anh0ang.github.io/abhakliste/).
