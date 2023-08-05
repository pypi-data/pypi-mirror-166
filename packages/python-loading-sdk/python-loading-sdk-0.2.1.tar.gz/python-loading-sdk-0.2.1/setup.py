# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['loading_sdk', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'python-loading-sdk',
    'version': '0.2.1',
    'description': 'Python api wrapper for loading.se',
    'long_description': '# Python Loading SDK\n\n[![PyPI Version][pypi-image]][pypi-url]\n[![][versions-image]][versions-url]\n[![Build Status][build-image]][build-url]\n\n[pypi-image]: https://img.shields.io/pypi/v/python-loading-sdk\n[pypi-url]: https://pypi.org/project/python-loading-sdk/\n[versions-image]: https://img.shields.io/pypi/pyversions/python-loading-sdk\n[versions-url]: https://pypi.org/project/python-loading-sdk/\n[build-image]: https://github.com/hnrkcode/python-loading-sdk/actions/workflows/build.yaml/badge.svg\n[build-url]: https://github.com/hnrkcode/python-loading-sdk/actions/workflows/build.yaml\n\n## Install\n\n```\npip install python-loading-sdk\n```\n\n## Usage\n\nInstantiate the client and optionally provide login credentials to be able to use methods that requires the user to be logged in.\n\n```python\nfrom loading_sdk import LoadingApiClient\n\nclient = LoadingApiClient(email="your@email.com", password="your_password")\n\nresponse = client.get_profile()\n```\n\nIt can also be used asyncrounously usage:\n```python\nfrom loading_sdk import AsyncLoadingApiClient\n\nclient = await AsyncLoadingApiClient(email="your@email.com", password="your_password")\n\nresponse = await client.get_profile()\n```\n\n## Examples\n\n### Requires Auth\n\n```python\nresponse = client.get_profile()\n```\n\n```python\nresponse = client.create_post(thread_id="5bbb986af1deda001d33bc4b", message="My message!")\n```\n\n```python\nresponse = client.edit_post(post_id="5bc876dd70a79c001dab7ebe", message="My updated message!")\n```\n\n```python\nresponse = client.create_thread(title="My title", message="The content!", category_name="games")\n```\n\n```python\nresponse = client.edit_thread(post_id="5bbb986af1deda001d33bc4b", message="My updated message!")\n```\n\n### Anonymous\n\n```python\nresponse = client.search(query="search query")\n```\n\n```python\nresponse = client.get_post(post_id="5bc876dd70a79c001dab7ebe")\n```\n\n```python\nresponse = client.get_thread(thread_id="5bbb986af1deda001d33bc4b", page=3)\n```\n\n```python\nresponse = client.get_games(page=5)\n```\n\n```python\nresponse = client.get_other(page=7)\n```\n\n```python\nresponse = client.get_editorials(page=2, post_type="review", sort="title")\n```',
    'author': 'hnrkcode',
    'author_email': '44243358+hnrkcode@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/hnrkcode/python-loading-sdk',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
