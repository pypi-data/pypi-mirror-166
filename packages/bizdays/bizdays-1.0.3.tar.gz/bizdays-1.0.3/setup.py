# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bizdays']
setup_kwargs = {
    'name': 'bizdays',
    'version': '1.0.3',
    'description': 'Functions to handle business days calculations',
    'long_description': "[![Downloads](https://img.shields.io/pypi/dm/bizdays.svg)](https://pypi.python.org/pypi/bizdays/)\n[![Latest Version](https://img.shields.io/pypi/v/bizdays.svg)](https://pypi.python.org/pypi/bizdays/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/bizdays.svg)](https://pypi.python.org/pypi/bizdays/)\n[![Development Status](https://img.shields.io/pypi/status/bizdays.svg)](https://pypi.python.org/pypi/bizdays/)\n\n# [python-bizdays](http://wilsonfreitas.github.io/python-bizdays/)\n\nIn several countries and markets, the accountability of the price of a financial\ninstrument, mainly bonds and derivatives, involves the use of different\nrules to compute the way the days go by.\nIn some countries, like in Brazil, several financial instrument only pay interest for business days along their life cycle.\nTherefore, having a way to compute the number of business days between 2 dates is quite useful to price the financial instruments properly.\nIt is necessary the holidays which occur between the 2 dates, to compute the business days and they are intrinsically related to counties and local markets.\nIn Brazil, [ANBIMA](http://portal.anbima.com.br/Pages/home.aspx) prepares a file with a list of holidays up to the year of 2078 which is largely used by market practioners for pricing financial instruments.\n<!-- Usually you have a list with the holidays and all you want\nis to find out the number of business days between two dates, nothing more. \nIt is necessary for pricing properly the financial instrument. -->\nSeveral financial libraries compute the holidays, giving no option to users set it by their own.\nFurtherly, the financial calendar is usually a small feature of a huge library, as [quantlib](http://quantlib.org/index.shtml), for example, and some users, including myself, don't want to put a hand in such a huge library only to use the financial calendar.\n\n**bizdays** is a pure Python module relying on its simplicity and the power of Python's batteries.\nbizdays computes business days between two dates and other collateral effects, like adjust a given date for the next or previous business day, check whether a date is a business day, creates generators of business days sequences, and so forth.\nbizdays is a module without further dependencies, what makes it appropriated for small implementations.\n\n",
    'author': 'wilsonfreitas',
    'author_email': 'wilson.freitas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
