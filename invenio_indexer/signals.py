# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Signals for indexer."""

from __future__ import absolute_import, print_function

from types import MethodType

from blinker import ANY, Namespace


def with_dynamic_connect(signal):
    """Adds a `dynamic_connect()` method to blinker signals."""
    def _dynamic_connect(self, receiver, sender=ANY, weak=True,
                         condition_func=None, **connect_kwargs):
        """Dynamically connect a receiver to a signal based on a condition."""
        def _default_condition_func(sender, connect_kwargs, **kwargs):
            return all(kwargs.get(k) == v for k, v in connect_kwargs.items())

        condition_func = condition_func or _default_condition_func

        def _conditional_receiver(sender, **kwargs):
            if condition_func(sender, connect_kwargs, **kwargs):
                receiver(sender, **kwargs)

        return self.connect(_conditional_receiver, sender=sender, weak=weak)

    signal.dynamic_connect = MethodType(_dynamic_connect, signal)
    return signal


_signals = Namespace()

before_record_index = with_dynamic_connect(
    _signals.signal('before-record-index'))
"""Signal sent before a record is indexed.

The sender is the current Flask application, and two keyword arguments are
provided:

- ``json``: The dumped record dictionary which can be modified.
- ``record``: The record being indexed.
- ``index``: The index in which the record will be indexed.
- ``doc_type``: The doc_type for the record.
- ``arguments``: The arguments to pass to Elasticsearch for indexing.
- ``**kwargs``: Extra arguments.
"""
