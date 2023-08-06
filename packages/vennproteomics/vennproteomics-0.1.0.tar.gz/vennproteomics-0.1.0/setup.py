# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vennproteomics']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib-venn>=0.11.7,<0.12.0',
 'matplotlib>=3.5.3,<4.0.0',
 'pandas>=1.4.4,<2.0.0',
 'uniprotparser>=1.0.8,<2.0.0']

setup_kwargs = {
    'name': 'vennproteomics',
    'version': '0.1.0',
    'description': 'Create Venn Diagram of Gene Names',
    'long_description': '## VennProteomics\n\n---\n\nFor creating venndiagram from gene names. VennProteomics also support reading in uniprot accession id and retrieve gene names from uniprot for the purpose of creating the venn-diagram.',
    'author': 'Toan K. Phung',
    'author_email': 'toan.phungkhoiquoctoan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noatgnu/vennProteomics',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
