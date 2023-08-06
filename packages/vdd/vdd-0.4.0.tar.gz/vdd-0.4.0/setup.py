# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vdd',
 'vdd.coda',
 'vdd.coda.tests',
 'vdd.common',
 'vdd.common.tests',
 'vdd.requirements',
 'vdd.requirements.tests']

package_data = \
{'': ['*'],
 'vdd': ['docs/*', 'docs/.ipynb_checkpoints/*'],
 'vdd.coda': ['data/*'],
 'vdd.coda.tests': ['data/*'],
 'vdd.requirements.tests': ['fixtures/*']}

install_requires = \
['numpy',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas',
 'platformdirs>=2.5.2,<3.0.0',
 'pygsheets>=2.0.5,<3.0.0',
 'pytz>=2022.2.1,<2023.0.0',
 'xlrd>=2.0,<3.0']

setup_kwargs = {
    'name': 'vdd',
    'version': '0.4.0',
    'description': 'Tools for Value-Driven Design',
    'long_description': 'Tools for Value-Driven Design\n=============================\n\n[![Build Status][master-build-status]][azure-pipeline]\n\n\nTools intended to help with modelling decisions in a value centric\ndesign process. The intent is to keep this as generic as possible, as\nsome of this decision modelling is suited to generic decision-making,\nnon-design activities with a little massaging.\n\n\nFeatures\n-------\n\n  - Concept Design Analysis (CODA) method implementation\n  - Requirements weighting with a Binary Weighting Matrix\n  - Programmatic or Spreadsheet based model creation (via Excel\n    workbooks or Google Sheets).\n\n\nInstall\n-------\n\n    pip install vdd\n\n\nDocumentation\n-------\n\nCurrently just stored in the repo.\n\n  - [Using Google Sheets for requirements matrices][binwm-gsheets]\n  - tbc\n\n\nDevelopment\n-----------\n\n`poetry` must be installed in the local development environment as a pre-requisite. In the repository root:\n\n\n\tpoetry install\n\n\n### Versioning\n\nSimple versioning approach: set the version in `pyproject.toml` and let poetry handle it.\n\n\nRoadmap\n-------\n\n![Azure DevOps builds (branch)][develop-build-status]\n\n  - Model sets for comparative work (rather than a single set of\n\tcharacteristic parameter values)\n  - Improved visualisation\n  - Export CODA models to Excel template\n  - House of Quality style requirement/characteristic weighting\n  - Pandas everywhere (v1.x)\n\n\nReferences\n----------\n\nBased on my own degree notes and open access literature:\n\n  - M.H. Eres et al, 2014. Mapping Customer Needs to Engineering\n\tCharacteristics: An Aerospace Perspective for Conceptual Design -\n\tJournal of Engineering Design pp. 1-24\n\t<http://eprints.soton.ac.uk/id/eprint/361442>\n\n<!-- statuses -->\n[azure-pipeline]: https://dev.azure.com/corriander/github-public/_build/latest?definitionId=2&branchName=master\n[master-build-status]: https://dev.azure.com/corriander/github-public/_apis/build/status/corriander.vdd?branchName=master\n[develop-build-status]: https://img.shields.io/azure-devops/build/corriander/8c97c580-4bf1-4e14-80b2-1be44ecc86f6/2/develop?label=develop\n[binwm-gsheets]: ./docs/gsheets-integration.md\n',
    'author': 'Alex Corrie',
    'author_email': 'ajccode@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
