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

from flask import current_app
from invenio_search import current_search
from invenio_search.utils import build_index_from_parts


def schema_to_index(schema, index_names=None):
    """Get index/doc_type given a schema URL.

    :param schema: The schema name
    :param index_names: A list of index name.
    :returns: A tuple containing (index, doc_type).
    """
    parts = schema.split("/")
    doc_type, ext = os.path.splitext(parts[-1])
    parts[-1] = doc_type
    doc_type = "_doc"

    if ext not in {
        ".json",
    }:
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
    schema = record.get("$schema", "")
    if isinstance(schema, dict):
        schema = schema.get("$ref", "")

    index, doc_type = schema_to_index(schema, index_names=index_names)

    if not (index and doc_type):
        index, doc_type = (
            current_app.config["INDEXER_DEFAULT_INDEX"],
            current_app.config["INDEXER_DEFAULT_DOC_TYPE"],
        )

    return index, "_doc"
