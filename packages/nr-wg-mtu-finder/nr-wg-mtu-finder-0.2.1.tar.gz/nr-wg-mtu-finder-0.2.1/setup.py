# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nr_wg_mtu_finder']

package_data = \
{'': ['*']}

install_requires = \
['flask==2.0.3',
 'matplotlib==3.4.3',
 'pandas==1.3.5',
 'pydantic==1.8.2',
 'requests==2.27.1',
 'seaborn==0.11.2',
 'werkzeug==2.0.3']

entry_points = \
{'console_scripts': ['nr-wg-mtu-finder = nr_wg_mtu_finder.main:run',
                     'nr-wg-mtu-finder-heatmap = '
                     'nr_wg_mtu_finder.main_heatmap:run']}

setup_kwargs = {
    'name': 'nr-wg-mtu-finder',
    'version': '0.2.1',
    'description': 'Scripts to find the optimal MTU for Wireguard server and peers.',
    'long_description': None,
    'author': 'nitred',
    'author_email': 'nitish.k.reddy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
