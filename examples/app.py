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
from os import environ, makedirs
import base64
from os.path import dirname, exists, join

from flask import Flask
from flask_celeryext import FlaskCeleryExt
from invenio_db import InvenioDB, db
from invenio_records import InvenioRecords
from invenio_records_files.api import Record
from invenio_search import InvenioSearch

from invenio_indexer import InvenioIndexer, signals

from invenio_files_rest import InvenioFilesREST
from invenio_files_rest.models import Bucket, FileInstance, Location, \
    MultipartObject, ObjectVersion, Part
import shutil

from flask import current_app
from io import BytesIO
from invenio_records_files.models import RecordsBuckets

# Create Flask application
index_name = 'testrecords-testrecord-v1.0.0'
app = Flask(__name__)
app.config.update(
    DATADIR=join(dirname(__file__), 'storage'),
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
InvenioFilesREST(app)
search = InvenioSearch(app)
search.register_mappings('testrecords', 'data')
InvenioIndexer(app)


@signals.before_record_index.connect_via(app)
def full_text_indexer(sender, json=None, record=None, index=None,
                      doc_type=None):
    return


@app.cli.group()
def fixtures():
    """Command for working with test data."""


@fixtures.command()
def files():
    """Load files."""
    d = current_app.config['DATADIR']
    if exists(d):
        shutil.rmtree(d)
    makedirs(d)

    # Clear data
    Part.query.delete()
    MultipartObject.query.delete()
    ObjectVersion.query.delete()
    Bucket.query.delete()
    FileInstance.query.delete()
    Location.query.delete()
    db.session.commit()

    # Create location
    loc = Location(name='local', uri=d, default=True)
    db.session.commit()

    # Bucket 0
    b1 = Bucket.create(loc)
    b1.id = '00000000-0000-0000-0000-000000000000'
    db.session.commit()


@fixtures.command()
def records():
    """Load test data fixture."""
    bucket = Bucket.query.get('00000000-0000-0000-0000-000000000000')
    with db.session.begin_nested():
        for idx in range(20):
            # create the record
            record = Record.create({
                'title': 'LHC experiment {}'.format(idx),
                'description': 'Data from experiment {}.'.format(idx),
                'type': 'data',
            })

            RecordsBuckets.create(bucket=bucket, record=record.model)

            record.files["key"] = BytesIO(b'hello world')
            record['_files'] = record.files.dumps()
            record['_files'][0]['file'] = {
                "_content": base64.b64encode(b'hwllo world').decode('utf-8'),
                "_indexed_chars": -1,
            }
            record.commit()

    db.session.commit()
