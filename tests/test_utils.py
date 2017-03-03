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


"""Test record indexing."""

from __future__ import absolute_import, print_function

from click.testing import CliRunner
from flask.cli import ScriptInfo
from flask_sqlalchemy import models_committed
from invenio_db import db
from invenio_search.cli import index as cmd
from invenio_search.proxies import current_search_client

from invenio_indexer.api import RecordIndexer
from invenio_indexer.signals import before_record_index
from invenio_indexer.utils import process_models_committed_signal


def test_record_indexing(app, queue):
    """Run record autoindexer."""
    @before_record_index.connect_via(app)
    def remove_schema(sender, json=None, record=None, **kwargs):
        if '$schema' in json:
            del json['$schema']

    with app.app_context():
        # NOTE: We have to use `db.get_app()` because Flask-SQLAlchemy v2.2
        # changed the way it picks a sender for the model signals.
        models_committed.connect(process_models_committed_signal,
                                 sender=db.get_app())
    with app.app_context():

        current_search_client.indices.delete_alias('_all', '_all',
                                                   ignore=[400, 404])
        current_search_client.indices.delete('*')
        aliases = current_search_client.indices.get_alias()
        assert 0 == len(aliases)

    runner = CliRunner()
    script_info = ScriptInfo(create_app=lambda info: app)

    with runner.isolated_filesystem():
        result = runner.invoke(cmd, ['destroy', '--yes-i-know'],
                               obj=script_info)
        result = runner.invoke(cmd, ['init'],
                               obj=script_info)
        assert 0 == result.exit_code

    with app.app_context():
        from invenio_records.models import RecordMetadata
        with db.session.begin_nested():
            record1 = RecordMetadata(json={
                '$schema': ('http://example.com/schemas/'  # external site
                            'records/default-v1.0.0.json'),
                'title': 'Test1',
            })
            db.session.add(record1)
            record2 = RecordMetadata(json={
                '$schema': ('http://example.com/schemas/'  # external site
                            'records/default-v1.0.0.json'),
                'title': 'Test2',
            })
            db.session.add(record2)
        db.session.commit()

        record_indexer = RecordIndexer(queue=queue)
        result = record_indexer.process_bulk_queue()
        assert (2, 0) == result

        response = current_search_client.get(
            index='records-default-v1.0.0',
            id=record1.id,
        )
        assert str(record1.id) == response['_id']

        response = current_search_client.get(
            index='records-default-v1.0.0',
            id=record2.id,
        )
        assert str(record2.id) == response['_id']

        db.session.delete(record1)
        db.session.commit()

        record_indexer.process_bulk_queue()

        response = current_search_client.get(
            index='records-default-v1.0.0',
            id=record1.id,
            ignore=404,
        )
        assert not response['found']

    # Clean-up:
    with app.app_context():
        result = runner.invoke(cmd, ['destroy', '--yes-i-know'],
                               obj=script_info)
        assert 0 == result.exit_code
