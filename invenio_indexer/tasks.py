# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks to index records."""

from __future__ import absolute_import, print_function

from celery import shared_task

from .api import RecordIndexer


@shared_task(ignore_result=True)
def process_bulk_queue(version_type=None, es_bulk_kwargs=None,
                       constructor_params=dict()):
    """Process bulk indexing queue.

    :param str version_type: Elasticsearch version type.
    :param dict es_bulk_kwargs: Passed to
        :func:`elasticsearch:elasticsearch.helpers.bulk`.
    :param dict constructor_params: Passed to RecordIndexer class.

    Note: You can start multiple versions of this task.
    """
    constructor_params[version_type] = version_type
    RecordIndexer(**constructor_params).process_bulk_queue(
        es_bulk_kwargs=es_bulk_kwargs)


@shared_task(ignore_result=True)
def index_record(record_uuid, constructor_params=dict()):
    """Index a single record.

    :param record_uuid: The record UUID.
    :param dict constructor_params: Passed to RecordIndexer class.
    """
    RecordIndexer(**constructor_params).index_by_id(record_uuid)


@shared_task(ignore_result=True)
def delete_record(record_uuid, constructor_params=dict()):
    """Delete a single record.

    :param record_uuid: The record UUID.
    :param dict constructor_params: Passed to RecordIndexer class.
    """
    RecordIndexer(**constructor_params).delete_by_id(record_uuid)
