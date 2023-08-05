# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pydiverse',
 'pydiverse.transform',
 'pydiverse.transform.core',
 'pydiverse.transform.core.expressions',
 'pydiverse.transform.core.ops',
 'pydiverse.transform.core.util',
 'pydiverse.transform.eager',
 'pydiverse.transform.lazy',
 'pydiverse.transform.util']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.4.39,<2.0.0', 'numpy>=1.23.1,<2.0.0', 'pandas>=1.4.3,<2.0.0']

extras_require = \
{'docs': ['Sphinx>=5.1.1,<6.0.0',
          'sphinx-rtd-theme>=1.0.0,<2.0.0',
          'sphinxcontrib-apidoc>=0.3.0,<0.4.0']}

setup_kwargs = {
    'name': 'pydiverse-transform',
    'version': '0.1.0',
    'description': 'Pipe based dataframe manipulation library that can also transform data on SQL databases',
    'long_description': '# pydiverse.transform\n\n[![CI](https://github.com/pydiverse/pydiverse.transform/actions/workflows/ci.yml/badge.svg)](https://github.com/pydiverse/pydiverse.transform/actions/workflows/ci.yml)\n\nPipe based dataframe manipulation library that can also transform data on SQL databases\n\n## Installation\n\nTo install the package locally in development mode, you first have to install\n[Poetry](https://python-poetry.org/docs/#installation).\nAfter that, install pydiverse transform like this:\n\n```bash\ngit clone https://github.com/pydiverse/pydiverse.transform.git\ncd pydiverse.transform\n\n# Create the environment, activate it and install the pre-commit hooks\npoetry install\npoetry shell\npre-commit install\n```\n',
    'author': 'QuantCo, Inc.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
