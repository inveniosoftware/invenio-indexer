# SPDX-FileCopyrightText: 2016-2022 CERN.
# SPDX-License-Identifier: MIT

"""Test celery task."""

import uuid
from unittest.mock import patch

from invenio_indexer.tasks import delete_record, index_record, process_bulk_queue


def test_process_bulk_queue(app):
    """Test index records."""
    with patch("invenio_indexer.api.RecordIndexer.process_bulk_queue") as fun:
        process_bulk_queue.delay()
        assert fun.called


def test_index_record(app):
    """Test index records."""
    with patch("invenio_indexer.api.RecordIndexer.index_by_id") as fun:
        recid = str(uuid.uuid4())
        index_record.delay(recid)
        fun.assert_called_with(recid)


def test_delete_record(app):
    """Test index records."""
    with patch("invenio_indexer.api.RecordIndexer.delete_by_id") as fun:
        recid = str(uuid.uuid4())
        delete_record.delay(recid)
        fun.assert_called_with(recid)
