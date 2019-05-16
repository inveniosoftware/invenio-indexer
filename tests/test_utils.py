# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test API."""

from __future__ import absolute_import, print_function

from elasticsearch import VERSION as ES_VERSION
from mock import patch

from invenio_indexer.utils import es_bulk_param_compatibility


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
