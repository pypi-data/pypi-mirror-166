from setuptools import setup
from setuptools import find_packages


version='0.9.9'

description = """
Python module for working with SMSFly service
"""

long_description = """
Python module for working with the service of sending SMS and Viber messages
"""

license = 'MIT License, see LICENSE file'

setup(
    name='smsflyapi2',
    version=version,

    author='Eugene Brezitskiy',
    author_email='brezitskiy@ukr.net',

    description=description,
    long_description=long_description,

    packages=find_packages(
        where='src',
        include=['smsflyapi2', 'tests'],
    ),
    package_dir={"": "src"},

    install_requires=[
        'requests'
    ],

    url='https://github.com/e-sft/smsflyapi2',
    license=license,

    classifiers=[
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Communications :: Email',
        'Topic :: Office/Business',
        'Topic :: Software Development :: Bug Tracking',
    ]
)
