# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['shoulder', 'shoulder.glenoid', 'shoulder.humerus']

package_data = \
{'': ['*']}

install_requires = \
['Rtree>=1.0.0,<2.0.0',
 'Shapely>=1.8.4,<2.0.0',
 'circle-fit>=0.1.3,<0.2.0',
 'networkx>=2.8.6,<3.0.0',
 'numpy-stl>=2.17.1,<3.0.0',
 'pandas>=1.4.4,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'scikit-spatial>=6.5.0,<7.0.0',
 'scipy>=1.9.1,<2.0.0',
 'trimesh>=3.14.1,<4.0.0']

setup_kwargs = {
    'name': 'shoulder',
    'version': '0.0.1',
    'description': 'patient specific anatomic coordinate system generation for shoulder bones',
    'long_description': '### Humeral Coordinate Systems\n\nGiven a 3d .stl model of the humerus finds the 3 axes (canal, transepicondylar, head central) and the articular margin plane.\n\nAlso reports the version and anatomic neck shaft angle.',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
