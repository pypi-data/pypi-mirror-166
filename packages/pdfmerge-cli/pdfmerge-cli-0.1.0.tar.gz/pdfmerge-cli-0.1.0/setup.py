# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pdfmerge']

package_data = \
{'': ['*']}

install_requires = \
['PyPDF2>=2.10.4,<3.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['pdfmerge = pdfmerge.main:pdf_merge']}

setup_kwargs = {
    'name': 'pdfmerge-cli',
    'version': '0.1.0',
    'description': 'pdf merge command line',
    'long_description': '# PDF Merge Tool\n\n## Build\n\n```bash\n$ poetry build\n$ pip install dist/pdfmerge-0.1.0.tar.gz\n```\n\n## Usage\n\n```bash\n$ pdfmerge  --input-dir .\n```\n\n## Refs\n\n- [py-pdf/PyPDF2](https://github.com/py-pdf/PyPDF2)\n',
    'author': 'maguowei',
    'author_email': 'i.maguowei@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/maguowei/pdfmerge',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
