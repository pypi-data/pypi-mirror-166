# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pools_dashboard']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.9.1,<5.0.0',
 'numpy>=1.23.2,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.3,<2.0.0',
 'plotly>=5.10.0,<6.0.0',
 'streamlit>=1.12.2,<2.0.0',
 'tabula-py>=2.5.0,<3.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'pools-dashboard',
    'version': '0.1.1',
    'description': 'analyze bets',
    'long_description': '# pools-analytics\n\n### Deployed at\nhttps://galenhew-pool-analytics-srcpools-dashboarddashboard-3ao0eg.streamlitapp.com/\n\n### Scope\n1. dashboard for bets \n2. poisson odds model\n3. other models\n4. add DB \n\n### Code\n- FE prototyping on streamlit\n\n- to install dependencies via poetry\n  - ```poetry install```\n\n- to run streamlit locally\n  - ```streamlit run dashboard.py ```\n\n',
    'author': 'ghew',
    'author_email': 'galenhew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/galenhew/pool-analytics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8, !=2.7.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, !=3.6.*, !=3.7.*',
}


setup(**setup_kwargs)
