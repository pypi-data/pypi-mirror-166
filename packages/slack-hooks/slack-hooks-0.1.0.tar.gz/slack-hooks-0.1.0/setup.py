# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webhooks', 'webhooks.blocks']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'slack-hooks',
    'version': '0.1.0',
    'description': 'Slack client for webhooks with Block Kit builder.',
    'long_description': ' # slack-hooks\n\n[![Version](https://img.shields.io/pypi/v/slack-hooks?logo=pypi)](https://pypi.org/project/slack-hooks)\n[![Quality Gate Status](https://img.shields.io/sonar/alert_status/fedecalendino_slack-hooks?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_slack-hooks)\n[![CodeCoverage](https://img.shields.io/sonar/coverage/fedecalendino_slack-hooks?logo=sonarcloud&server=https://sonarcloud.io)](https://sonarcloud.io/dashboard?id=fedecalendino_slack-hooks)\n',
    'author': 'Fede Calendino',
    'author_email': 'fede@calendino.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedecalendino/slack-hooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
