# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonemoji']

package_data = \
{'': ['*']}

install_requires = \
['noneprompt>=0.1.3,<0.2.0']

entry_points = \
{'console_scripts': ['nonemoji = nonemoji.__main__:main']}

setup_kwargs = {
    'name': 'nonemoji',
    'version': '0.1.3',
    'description': 'Simple gitmoji cli written in python',
    'long_description': '# Nonemoji\n\n自维护的 gitmoji-cli，删减了部分 emoji\n\n## 安装\n\n```bash\npoetry add nonemoji --dev\n```\n\n## pre-commit 使用\n\n```yaml\n# .pre-commit-config.yaml\ndefault_install_hook_types: [pre-commit, prepare-commit-msg]\nrepos:\n  - repo: https://github.com/pycqa/isort\n    rev: 5.10.1\n    hooks:\n      - id: isort\n        stages: [commit]\n\n  - repo: https://github.com/psf/black\n    rev: 22.6.0\n    hooks:\n      - id: black\n        stages: [commit]\n\n  - repo: https://github.com/nonebot/nonemoji\n    rev: v0.1.1\n    hooks:\n      - id: nonemoji\n```\n',
    'author': 'jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
