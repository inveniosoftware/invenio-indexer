# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016, 2017 CERN.
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

"""Record indexer for Invenio."""

from __future__ import absolute_import, print_function

from kombu import Exchange, Queue

INDEXER_DEFAULT_INDEX = "records-record-v1.0.0"
"""Default index to use if no schema is defined."""

INDEXER_DEFAULT_DOC_TYPE = "record-v1.0.0"
"""Default doc_type to use if no schema is defined."""

INDEXER_MQ_EXCHANGE = Exchange('indexer', type='direct')
"""Default exchange for message queue."""

INDEXER_MQ_QUEUE = Queue(
    'indexer', exchange=INDEXER_MQ_EXCHANGE, routing_key='indexer')
"""Default queue for message queue."""

INDEXER_MQ_ROUTING_KEY = 'indexer'
"""Default routing key for message queue."""

INDEXER_REPLACE_REFS = True
"""Whether to replace JSONRefs prior to indexing record."""

INDEXER_BULK_REQUEST_TIMEOUT = 10
"""Request timeout to use in Bulk indexing."""

INDEXER_RECORD_TO_INDEX = 'invenio_indexer.utils.default_record_to_index'
"""Provide an implemetation of record_to_index function"""

INDEXER_BEFORE_INDEX_HOOKS = []
"""List of automatically connected hooks (function or importable string)."""
