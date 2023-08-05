# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['api66jenkins']

package_data = \
{'': ['*']}

install_requires = \
['api4jenkins>=1.12,<2.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'api66jenkins',
    'version': '0.0.6',
    'description': 'Python3 client library for Jenkins API. Adding a keyword from api4jenkins  add job.build [custom] parameter',
    'long_description': '\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/api4jenkins)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/api4jenkins)\n[![Documentation Status](https://readthedocs.org/projects/api4jenkins/badge/?version=latest)](https://api4jenkins.readthedocs.io/en/latest/?badge=latest)\n![GitHub](https://img.shields.io/github/license/joelee2012/api4jenkins)\n\n\n# Jenkins Python Client\n\n[Python3](https://www.python.org/) client library for [Jenkins API](https://wiki.jenkins.io/display/JENKINS/Remote+access+API). \n\ndispose api4jenkins job.  Build could not pass dictionary format。\n\nThanks to the original authors of api4jenkins for providing such a nice package to manipulate Jenkins\n\n# Features\n\n- Object oriented, each Jenkins item has corresponding class, easy to use and extend\n- Base on `api/json`, easy to query/filter attribute of item\n- Setup relationship between class just like Jenkins item\n- Support api for almost every Jenkins item\n- Pythonic\n- Test with latest Jenkins LTS\n\n# Installation\n\n```bash\npython3 -m pip install api66jenkins\n```\n\n# Quick start\n\n```python\n>>> from api66jenkins import Jenkins\n>>> client = Jenkins(\'http://127.0.0.1:8080/\', auth=(\'admin\', \'admin\'))\n>>> client.version\n\'2.176.2\'\n>>> xml = """<?xml version=\'1.1\' encoding=\'UTF-8\'?>\n... <project>\n...   <builders>\n...     <hudson.tasks.Shell>\n...       <command>echo $JENKINS_VERSION</command>\n...     </hudson.tasks.Shell>\n...   </builders>\n... </project>"""\n>>> client.create_job(\'path/to/job\', xml)\n>>> import time\n>>> item = client.build_job(\'path/to/job\')\n>>> while not item.get_build():\n...      time.sleep(1)\n>>> build = item.get_build()\n>>> for line in build.progressive_output():\n...     print(line)\n...\nStarted by user admin\nRunning as SYSTEM\nBuilding in workspace /var/jenkins_home/workspace/freestylejob\n[freestylejob] $ /bin/sh -xe /tmp/jenkins2989549474028065940.sh\n+ echo $JENKINS_VERSION\n2.176.2\nFinished: SUCCESS\n>>> build.building\nFalse\n>>> build.result\n\'SUCCESS\'\n```\n\n# Documentation\nUser Guide and API Reference is available on [Read the Docs](https://api4jenkins.readthedocs.io/)\n\n',
    'author': 'sanmejie',
    'author_email': 'liyapong@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
