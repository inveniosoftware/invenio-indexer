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

"""Test CLI."""

from __future__ import absolute_import, print_function

import uuid
from time import sleep

from click.testing import CliRunner
from invenio_db import db
from invenio_pidstore.minters import recid_minter
from invenio_records import Record
from invenio_search import current_search_client

from invenio_indexer import cli
from invenio_indexer.api import RecordIndexer


def test_run(script_info):
    """Test run."""
    runner = CliRunner()
    res = runner.invoke(cli.run, [], obj=script_info)
    assert res.exit_code == 0

    runner = CliRunner()
    res = runner.invoke(cli.run, ['-d', '-c', '2'], obj=script_info)
    assert res.exit_code == 0
    assert 'Starting 2 tasks' in res.output


def test_reindex(app, script_info, queue):
    """Test reindex."""
    # load records
    with app.test_request_context():
        runner = CliRunner()

        schema = {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'field': {'type': 'boolean'},
            },
            'required': ['title'],
        }

        rec_uuid = uuid.uuid4()
        data = {'title': 'Test0', '$schema': schema}
        recid_minter(rec_uuid, data)
        record = Record.create(data, id_=rec_uuid)
        db.session.commit()

        runner.invoke(cli.reindex, ['recid'], obj=script_info)
        runner.invoke(cli.run, [], obj=script_info)
        sleep(5)
        indexer = RecordIndexer()
        index, doc_type = indexer.record_to_index(record)
        current_search_client.get(index=index, doc_type=doc_type,
                                  id=rec_uuid)
