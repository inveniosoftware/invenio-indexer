# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utility functions for data processing."""

import os
from functools import wraps

import six
from elasticsearch import VERSION as ES_VERSION
from flask import current_app
from invenio_search import current_search
from invenio_search.utils import build_index_from_parts


def schema_to_index(schema, index_names=None):
    """Get index/doc_type given a schema URL.

    :param schema: The schema name
    :param index_names: A list of index name.
    :returns: A tuple containing (index, doc_type).
    """
    parts = schema.split('/')
    doc_type, ext = os.path.splitext(parts[-1])
    parts[-1] = doc_type
    if ES_VERSION[0] >= 7:
        doc_type = '_doc'

    if ext not in {'.json', }:
        return (None, None)

    if index_names is None:
        index = build_index_from_parts(*parts)
        return index, doc_type

    for start in range(len(parts)):
        name = build_index_from_parts(*parts[start:])
        if name in index_names:
            return name, doc_type

    return (None, None)


def default_record_to_index(record):
    """Get index/doc_type given a record.

    It tries to extract from `record['$schema']` the index and doc_type.
    If it fails, return the default values.

    :param record: The record object.
    :returns: Tuple (index, doc_type).
    """
    index_names = current_search.mappings.keys()
    schema = record.get('$schema', '')
    if isinstance(schema, dict):
        schema = schema.get('$ref', '')

    index, doc_type = schema_to_index(schema, index_names=index_names)

    if not (index and doc_type):
        index, doc_type = (
            current_app.config['INDEXER_DEFAULT_INDEX'],
            current_app.config['INDEXER_DEFAULT_DOC_TYPE'],
        )

    if ES_VERSION[0] >= 7:
        doc_type = '_doc'

    return index, doc_type


# NOTE: Remove when https://github.com/elastic/elasticsearch-py/pull/1062 is
# merged.
def _es7_expand_action(data):
    """ES7-compatible bulk action expand."""
    # when given a string, assume user wants to index raw json
    if isinstance(data, six.string_types):
        return '{"index":{}}', data

    # make sure we don't alter the action
    data = data.copy()
    op_type = data.pop("_op_type", "index")
    action = {op_type: {}}
    for key in (
        "_id",
        "_index",
        "_parent",
        "_percolate",
        "_retry_on_conflict",
        "_routing",
        "_timestamp",
        "_type",
        "_version",
        "_version_type",
        "parent",
        "pipeline",
        "retry_on_conflict",
        "routing",
        "version",
        "version_type",
    ):
        if key in data:
            if key in (
                "_parent",
                "_retry_on_conflict",
                "_routing",
                "_version",
                "_version_type",
            ):
                action[op_type][key[1:]] = data.pop(key)
            else:
                action[op_type][key] = data.pop(key)

    # no data payload for delete
    if op_type == "delete":
        return action, None

    return action, data.get("_source", data)
