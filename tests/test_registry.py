# SPDX-FileCopyrightText: 2022 CERN.
# SPDX-License-Identifier: MIT

"""Indexer registry module tests."""

import pytest

from invenio_indexer.api import RecordIndexer
from invenio_indexer.proxies import current_indexer_registry


def test_indexer_registry(app):
    indexer_instance = RecordIndexer()
    current_indexer_registry.register(indexer_instance, "test")

    # fail on duplicate id
    pytest.raises(
        RuntimeError, current_indexer_registry.register, indexer_instance, "test"
    )
    # get indexer
    assert indexer_instance == current_indexer_registry.get("test")
    # get id
    assert "test" == current_indexer_registry.get_indexer_id(indexer_instance)
    # get id of non-registered indexer
    pytest.raises(KeyError, current_indexer_registry.get_indexer_id, RecordIndexer())
    # add a second one and get the list
    current_indexer_registry.register(indexer_instance, "test_too")
    indexers = current_indexer_registry.all().keys()
    assert not set(indexers).difference({"test", "test_too"})
