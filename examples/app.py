# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.


r"""Minimal Flask application example for development.

Run ElasticSearch and RabbitMQ server and then run example development server:

.. code-block:: console

    $ pip install -e .[all]
    $ cd examples
    $ ./app-setup.sh
    $ ./app-fixtures.sh

Try to get some records:

.. code-block:: console

    $ curl -X GET localhost:9200/_cat/indices?v
    $ curl -X GET localhost:9200/testrecords-testrecord-v1.0.0/_search | \
        python -m json.tool

To be able to uninstall the example app:

.. code-block:: console

    $ ./app-teardown.sh

"""

from __future__ import absolute_import, print_function

import os
import uuid

from flask import Flask
from flask_celeryext import FlaskCeleryExt
from invenio_db import InvenioDB, db
from invenio_pidstore.models import PersistentIdentifier, PIDStatus
from invenio_records import InvenioRecords
from invenio_records.api import Record
from invenio_search import InvenioSearch

from invenio_indexer import InvenioIndexer

# Create Flask application
index_name = 'testrecords-testrecord-v1.0.0'
app = Flask(__name__)
app.config.update(
    CELERY_ALWAYS_EAGER=True,
    CELERY_CACHE_BACKEND='memory',
    CELERY_EAGER_PROPAGATES_EXCEPTIONS=True,
    CELERY_RESULT_BACKEND='cache',
    INDEXER_DEFAULT_DOC_TYPE='testrecord-v1.0.0',
    INDEXER_DEFAULT_INDEX=index_name,
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI',
                                      'sqlite:///app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
)

FlaskCeleryExt(app)
InvenioDB(app)
InvenioRecords(app)
search = InvenioSearch(app)
search.register_mappings('testrecords', 'data')
InvenioIndexer(app)


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def records():
    """Load test data fixture."""
    with db.session.begin_nested():
        for idx in range(20):
            # create the record
            id_ = uuid.uuid4()
            Record.create({
                'title': 'LHC experiment {}'.format(idx),
                'description': 'Data from experiment {}.'.format(idx),
                'type': 'data',
                'recid': idx
            }, id_=id_)
            PersistentIdentifier.create(
                pid_type='recid',
                pid_value=idx,
                object_type='rec',
                object_uuid=id_,
                status=PIDStatus.REGISTERED,
            )

    db.session.commit()
