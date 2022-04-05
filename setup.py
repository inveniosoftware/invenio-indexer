# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Record indexer for Invenio."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'attrs>=17.4.0',
    'pytest-invenio>=1.4.6',
    'redis>=3.4.0',
]

invenio_search_version = '1.4.0'

extras_require = {
    'docs': [
        'Sphinx>=4.2.0,<5',
    ],
    'elasticsearch6': [
        'invenio-search[elasticsearch6]>={}'.format(invenio_search_version),
    ],
    'elasticsearch7': [
        'invenio-search[elasticsearch7]>={}'.format(invenio_search_version),
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name[0] == ':' or name in ('elasticsearch6', 'elasticsearch7'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
]

install_requires = [
    'invenio-db>=1.0.14',
    'invenio-pidstore>=1.2.0',
    'invenio-records>=1.4.0',
    'pytz>=2016.4',
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_indexer', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-indexer',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio elasticsearch indexing',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-indexer',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'invenio_base.apps': [
            'invenio_indexer = invenio_indexer:InvenioIndexer',
        ],
        'invenio_base.api_apps': [
            'invenio_indexer = invenio_indexer:InvenioIndexer',
        ],
        'invenio_celery.tasks': [
            'invenio_indexer = invenio_indexer.tasks',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
