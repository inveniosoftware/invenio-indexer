# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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

"""Module tests."""

from __future__ import absolute_import, print_function

import uuid

import pytz
from flask import Flask
from invenio_db import db
from invenio_records import Record
from mock import MagicMock

from invenio_indexer import InvenioIndexer
from invenio_indexer.api import RecordIndexer

_global_magic_hook = MagicMock()
"""Iternal importable magic hook instance."""


def test_version():
    """Test version import."""
    from invenio_indexer import __version__
    assert __version__


def test_init():
    """Test extension initialization."""
    app = Flask('testapp')
    ext = InvenioIndexer(app)
    assert 'invenio-indexer' in app.extensions

    app = Flask('testapp')
    ext = InvenioIndexer()
    assert 'invenio-indexer' not in app.extensions
    ext.init_app(app)
    assert 'invenio-indexer' in app.extensions


def test_hook_initialization(base_app):
    """Test hook initialization."""
    app = base_app
    magic_hook = MagicMock()
    app.config['INDEXER_BEFORE_INDEX_HOOKS'] = [
        magic_hook, 'test_invenio_bulkindexer:_global_magic_hook'
    ]
    ext = InvenioIndexer(app)

    with app.app_context():
        recid = uuid.uuid4()
        record = Record.create({'title': 'Test'}, id_=recid)
        db.session.commit()

        client_mock = MagicMock()
        RecordIndexer(search_client=client_mock, version_type='force').index(
            record)
        args = (app, )
        kwargs = dict(
            index=app.config['INDEXER_DEFAULT_INDEX'],
            doc_type=app.config['INDEXER_DEFAULT_DOC_TYPE'],
            record=record,
            json={
                'title': 'Test',
                '_created': pytz.utc.localize(record.created).isoformat(),
                '_updated': pytz.utc.localize(record.updated).isoformat(),
            },
        )
        magic_hook.assert_called_with(*args, **kwargs)
        _global_magic_hook.assert_called_with(*args, **kwargs)
        client_mock.index.assert_called_with(
            id=str(recid),
            version=0,
            version_type='force',
            index=app.config['INDEXER_DEFAULT_INDEX'],
            doc_type=app.config['INDEXER_DEFAULT_DOC_TYPE'],
            body={
                'title': 'Test',
                '_created': pytz.utc.localize(record.created).isoformat(),
                '_updated': pytz.utc.localize(record.updated).isoformat(),
            },
        )
