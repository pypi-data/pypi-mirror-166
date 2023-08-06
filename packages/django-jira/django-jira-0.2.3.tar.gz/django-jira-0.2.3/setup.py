# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_jira',
 'django_jira.error_handler',
 'django_jira.error_handler.templates',
 'django_jira.tasks']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3.2.0,<4.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'djangorestframework>=3.13.1,<4.0.0',
 'jira>=3.4.1,<4.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'django-jira',
    'version': '0.2.3',
    'description': 'Intergrates Jira library into django microservices',
    'long_description': '# Django-Jira\n\nAllows for creating issues in Jira with Django RestFramework\n',
    'author': 'Antoine Wood',
    'author_email': 'antoinewood@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
