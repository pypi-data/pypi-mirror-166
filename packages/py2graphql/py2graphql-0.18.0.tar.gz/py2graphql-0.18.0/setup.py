# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py2graphql']

package_data = \
{'': ['*']}

install_requires = \
['addict>=2.2.1,<3.0.0',
 'aiohttp>=3.6.2,<4.0.0',
 'requests>=2.24.0,<3.0.0',
 'tenacity>=6.2.0,<7.0.0']

setup_kwargs = {
    'name': 'py2graphql',
    'version': '0.18.0',
    'description': 'Pythonic GraphQL Client',
    'long_description': 'py2graphql (Python to GraphQL)\n##############################\n\n|pypi|\n\n1. GraphQL\n2. Django queryset love\n3. ``__getattr__`` abuse\n4. ???\n5. Profit!!!\n\n\nWhat\n----\npy2graphql is a Python GraphQL client that makes GraphQL feel better to use. It almost feels like you\'re using Django\'s ORM.\n\n\nInstallation\n------------\n.. code-block:: bash\n   :class: ignore\n\n   pip install py2graphql\n\n\nExample\n-------\n\nThis Python equates to the following GraphQL.\n\n.. code-block:: python\n   :class: ignore\n\n   from py2graphql import Query\n\n   Query().repository(owner=\'juliuscaeser\', name=\'rome\').pullRequest(number=2).values(\'title\', \'url\').commits(last=250).edges.node.commit.values(\'id\', \'message\', \'messageBody\')\n\n.. code-block:: graphql\n   :class: ignore\n\n   query {\n     repository(owner: "juliuscaeser", name: "rome") {\n       pullRequest(number: 2) {\n         title\n         url\n         commits(last: 250) {\n           edges {\n             node {\n               commit {\n                 id\n                 message\n                 messageBody\n               }\n             }\n           }\n         }\n       }\n     }\n   }\n\nYou can even use the library to do the HTTP requests:\n\n.. code-block:: python\n   :class: ignore\n\n   from py2graphql import Client\n\n   headers = {\n       \'Authorization\': \'token MY_TOKEN\',\n   }\n   Client(url=THE_URL, headers=headers).query().repository(owner=\'juliuscaeser\', name=\'rome\').fetch()\n\nIt also supports Mutations:\n\n.. code-block:: python\n   :class: ignore\n\n   from py2graphql import Client, Query\n\n   headers = {\n       \'Authorization\': \'token MY_TOKEN\',\n   }\n   client = Client(url=THE_URL, headers=headers)\n   mutation = Query(name=\'mutation\', client=client)\n\n\nAnd multiple queries in a single request:\n\n.. code-block:: python\n   :class: ignore\n\n   from py2graphql import Client, Query\n\n   headers = {\n       \'Authorization\': \'token MY_TOKEN\',\n   }\n   query = Client(url=THE_URL, headers=headers).query().repository(owner=\'juliuscaeser\', name=\'rome\')\n   query.pullRequest(number=2).values(\'title\', \'url\')\n   query.releases(first=10).edges.node.values(\'name\')\n   query.get_graphql()\n\n.. code-block:: graphql\n   :class: ignore\n\n   query {\n     repository(owner: "juliuscaeser", name: "rome") {\n        pullRequest(number: 2) {\n          title\n          url\n        }\n        releases(first: 10) {\n          edges {\n            node {\n              name\n            }\n          }\n        }\n      }\n   }\n\nAs well as GraphQL errors:\n\n.. code-block:: python\n   :class: ignore\n\n   from py2graphql import Client, Query\n\n   headers = {\n       \'Authorization\': \'token MY_TOKEN\',\n   }\n   result = Client(url=THE_URL, headers=headers).query().repository(owner=\'juliuscaeser\', name=\'rome\').fetch()\n   result._errors\n   [{\'message\': "Field \'repository\' is missing required arguments: name", \'locations\': [{\'line\': 7, \'column\': 3}]}]\n\n\n.. |pypi| image:: https://img.shields.io/pypi/v/py2graphql.svg?style=flat\n   :target: https://pypi.python.org/pypi/py2graphql\n',
    'author': 'Willem Thiart',
    'author_email': 'himself@willemthiart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/willemt/py2graphql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
