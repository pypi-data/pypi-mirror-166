# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apollo_config_sdk']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'apollo-config-sdk',
    'version': '0.1.2',
    'description': '',
    'long_description': '# Apollo-Config-Sdk\n\n\n```python\nfrom apollo_config_sdk.client import ApolloClient\n\nif __name__ == \'__main__\':\n    client = ApolloClient(\n        app_id="appid",\n        cluster="cluster",\n        config_url=\'config_url\',\n        secret="secret"\n    )\n\n    for i in range(500):\n        import time\n\n        time.sleep(1)\n        z = client.get_value(\'key\', namespace=\'namespace\')\n        print(z)\n        pass\n```',
    'author': 'lishulong',
    'author_email': 'lishulong.never@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
