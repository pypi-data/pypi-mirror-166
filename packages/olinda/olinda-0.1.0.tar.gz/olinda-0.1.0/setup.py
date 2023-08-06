# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['olinda', 'olinda.cli', 'olinda.data', 'olinda.models', 'olinda.pipelines']

package_data = \
{'': ['*'], 'olinda': ['configs/*']}

install_requires = \
['cbor2>=5.4.3,<6.0.0',
 'cbor>=1.0.0,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'gin-config>=0.5.0,<0.6.0',
 'griddify>=0.0.1,<0.0.2',
 'joblib>=1.1.0,<2.0.0',
 'onnx-tf>=1.10.0,<2.0.0',
 'onnx>=1.12.0,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pydantic>=1.9.2,<2.0.0',
 'pytorch-lightning>=1.7.2,<2.0.0',
 'torch>=1.12.1,<2.0.0',
 'webdataset>=0.2.18,<0.3.0',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['olinda = olinda.cli.main:main']}

setup_kwargs = {
    'name': 'olinda',
    'version': '0.1.0',
    'description': 'A model distillation library',
    'long_description': None,
    'author': 'Ankur Kumar',
    'author_email': 'ank@leoank.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
