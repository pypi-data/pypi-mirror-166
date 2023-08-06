# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['camt_to_erpnext']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['camt-to-erpnext = camt_to_erpnext.main:app']}

setup_kwargs = {
    'name': 'camt-to-erpnext',
    'version': '0.1.0',
    'description': '',
    'long_description': '\nExpects a file in CSV-CAMT-Format, with the following columns:\n\n- Auftragskonto\n- Buchungstag\n- Valutadatum\n- Buchungstext\n- Verwendungszweck\n- Glaeubiger ID\n- Mandatsreferenz\n- Kundenreferenz (End-to-End)\n- Sammlerreferenz\n- Lastschrift Ursprungsbetrag\n- Auslagenersatz Ruecklastschrift\n- Beguenstigter/Zahlungspflichtiger\n- Kontonummer/IBAN\n- BIC (SWIFT-Code)\n- Betrag\n- Waehrung\n- Info\n\nOutputs a normal CSV file with the following columns:\n\n- Date\n- Deposit\n- Withdrawal\n- Description\n- Reference Number\n- Bank Account\n- Currency\n',
    'author': 'barredterra',
    'author_email': '14891507+barredterra@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
