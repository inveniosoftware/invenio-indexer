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

"""Test celery task."""

from __future__ import absolute_import, print_function

import uuid

from mock import patch

from invenio_indexer.tasks import delete_record, index_record, \
    process_bulk_queue


def test_process_bulk_queue(app):
    """Test index records."""
    with patch('invenio_indexer.api.RecordIndexer.process_bulk_queue') as fun:
        process_bulk_queue.delay()
        assert fun.called


def test_index_record(app):
    """Test index records."""
    with patch('invenio_indexer.api.RecordIndexer.index_by_id') as fun:
        recid = str(uuid.uuid4())
        index_record.delay(recid)
        fun.assert_called_with(recid)


def test_delete_record(app):
    """Test index records."""
    with patch('invenio_indexer.api.RecordIndexer.delete_by_id') as fun:
        recid = str(uuid.uuid4())
        delete_record.delay(recid)
        fun.assert_called_with(recid)
