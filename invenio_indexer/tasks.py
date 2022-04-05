# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2022 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks to index records."""

from celery import shared_task

from .api import RecordIndexer


@shared_task(ignore_result=True)
def process_bulk_queue(version_type=None, es_bulk_kwargs=None):
    """Process bulk indexing queue.

    :param str version_type: Elasticsearch version type.
    :param dict es_bulk_kwargs: Passed to
        :func:`elasticsearch:elasticsearch.helpers.bulk`.

    Note: You can start multiple versions of this task.
    """
    RecordIndexer(version_type=version_type).process_bulk_queue(
        es_bulk_kwargs=es_bulk_kwargs)


@shared_task(ignore_result=True)
def index_record(record_uuid):
    """Index a single record.

    :param record_uuid: The record UUID.
    """
    RecordIndexer().index_by_id(record_uuid)


@shared_task(ignore_result=True)
def delete_record(record_uuid):
    """Delete a single record.

    :param record_uuid: The record UUID.
    """
    RecordIndexer().delete_by_id(record_uuid)
