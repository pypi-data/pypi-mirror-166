from setuptools import setup, find_packages

setup(
    name="debitcr",
    version='0.0.3',
    author="Norma Escobar",
    author_email="norma@normaescobar.com",
    description="A python library that provides detailed wallet history and categorizes transactions as sent/received.",
    long_description='''
## Introduction
debitcr is a Python library that provides detailed wallet history and categorizes transactions as sent/received.
It was born from the need of organizing institutional-volume level of transactions.
All kudos to the Ethereum team of developers for the free APIs.

## Security
By default debitcr does not guard against quadratic blowup or billion laughs xml attacks. To guard against these install defusedxml.

## Documentation
The documentation is at: https://krpbtc.com

* installation methods
* supported blockchains
* how to contribute
    
    ''',
    packages=find_packages(),
    long_description_content_type='text/markdown',    
    install_requires=['openpyxl', 'requests']
)