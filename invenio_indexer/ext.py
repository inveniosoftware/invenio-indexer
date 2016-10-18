# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016 CERN.
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

"""Flask exension for Invenio-Indexer."""

from __future__ import absolute_import, print_function

import six
from flask import current_app
from werkzeug.utils import cached_property, import_string

from . import config
from .cli import run  # noqa
from .signals import before_record_index


class InvenioIndexer(object):
    """Invenio-Indexer extension."""

    def __init__(self, app=None):
        """Extension initialization.

        :param app: The Flask application. (Default: ``None``)
        """
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization.

        :param app: The Flask application.
        """
        self.init_config(app)
        app.extensions['invenio-indexer'] = self

        hooks = app.config.get('INDEXER_BEFORE_INDEX_HOOKS', [])
        for hook in hooks:
            if isinstance(hook, six.string_types):
                hook = import_string(hook)
            before_record_index.connect_via(app)(hook)

    def init_config(self, app):
        """Initialize configuration.

        :param app: The Flask application.
        """
        for k in dir(config):
            if k.startswith('INDEXER_'):
                app.config.setdefault(k, getattr(config, k))

    @cached_property
    def record_to_index(self):
        """Import the configurable 'record_to_index' function."""
        return import_string(current_app.config.get('INDEXER_RECORD_TO_INDEX'))
