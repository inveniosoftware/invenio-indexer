# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test API."""

from __future__ import absolute_import, print_function

import pytest
from elasticsearch import VERSION as ES_VERSION
from mock import patch

from invenio_indexer.utils import es_bulk_param_compatibility, schema_to_index


def test_schema_to_index_with_names(app):
    """Test that prefix is added to the index when creating it."""
    result = schema_to_index('default.json', index_names=['default'])
    assert result == (
        'default',
        '_doc' if ES_VERSION[0] >= 7 else 'default'
    )


@pytest.mark.parametrize(
    ('schema, expected, index_names'),
    (
        (
            'records/record-v1.0.0.json',
            ('records-record-v1.0.0', 'record-v1.0.0'),
            None,
        ),
        (
            '/records/record-v1.0.0.json',
            ('records-record-v1.0.0', 'record-v1.0.0'),
            None,
        ),
        (
            'default-v1.0.0.json',
            ('default-v1.0.0', 'default-v1.0.0'),
            None,
        ),
        (
            'default-v1.0.0.json',
            (None, None),
            [],
        ),
        (
            'invalidextension',
            (None, None),
            None,
        ),
    ),
)
def test_schema_to_index(schema, expected, index_names, app):
    """Test the expected value of schema to index."""
    result = schema_to_index(schema, index_names=index_names)
    if ES_VERSION[0] >= 7 and expected[0]:
        expected = (expected[0], '_doc')
    assert result == expected


def test_es6_bulk_param_compat(generate_action):
    """Test ES bulk param compatibility decorator."""
    action = {
        '_index': 'index',
        '_type': '_doc',
        'test': 'test',
        'opType': 'opType',
        'versionType': 'version type',
        '_parent': 'parent',
        '_retry_on_conflict': 'retry',
        '_routing': 'routing',
        '_version': 'version',
    }
    expected_action = {
        '_index': 'index',
        '_type': '_doc',
        'test': 'test',
        'opType': 'opType',
        'versionType': 'version type',
        '_parent': 'parent',
        '_retry_on_conflict': 'retry',
        '_routing': 'routing',
        '_version': 'version',
    }
    with patch('invenio_indexer.utils.ES_VERSION', (6, 3, 0)) as version:
        assert generate_action(action) == expected_action


def test_es7_bulk_param_compat(generate_action):
    """Test ES bulk param compatibility decorator."""
    action = {
        '_index': 'index',
        '_type': '_doc',
        'test': 'test',
        'opType': 'opType',
        'versionType': 'version type',
        '_parent': 'parent',
        '_retry_on_conflict': 'retry',
        '_routing': 'routing',
        '_version': 'version',
    }
    expected_action = {
        '_index': 'index',
        '_type': '_doc',
        'test': 'test',
        'op_type': 'opType',
        'version_type': 'version type',
        'parent': 'parent',
        'retry_on_conflict': 'retry',
        'routing': 'routing',
        'version': 'version',
    }
    with patch('invenio_indexer.utils.ES_VERSION', (7, 0, 1)) as version:
        assert generate_action(action) == expected_action
