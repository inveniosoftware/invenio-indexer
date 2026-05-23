# SPDX-FileCopyrightText: 2016-2022 CERN.
# SPDX-License-Identifier: MIT

"""Proxy objects for easier access to application objects."""

from flask import current_app
from werkzeug.local import LocalProxy


def _get_current_record_to_index():
    return current_app.extensions["invenio-indexer"].record_to_index


current_record_to_index = LocalProxy(_get_current_record_to_index)

current_indexer_registry = LocalProxy(
    lambda: current_app.extensions["invenio-indexer"].registry
)
"""Helper proxy to get the current indexer registry."""
