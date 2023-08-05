# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['daypy', 'daypy.plugins']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.2,<2.0.0']

setup_kwargs = {
    'name': 'daypy',
    'version': '0.1.5',
    'description': '一个日期时间解析器',
    'long_description': '# daypy',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mic1on/daypy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
