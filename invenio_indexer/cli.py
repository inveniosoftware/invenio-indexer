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

"""CLI for indexer."""

from __future__ import absolute_import, print_function

import click
from flask_cli import with_appcontext
from invenio_search.cli import index

from .api import RecordIndexer
from .tasks import process_bulk_queue


@index.command()
@click.option(
    '--delayed', '-d', is_flag=True, help="Run indexing in background.")
@click.option(
    '--concurrency', '-c', default=1, type=int,
    help="Number of concurrent indexing tasks to start.")
@with_appcontext
def run(delayed, concurrency):
    """Run bulk record indexing."""
    if delayed:
        click.secho(
            "Starting {0} tasks for indexing records...".format(concurrency),
            fg='green')
        for c in range(0, concurrency):
            process_bulk_queue.delay()
    else:
        click.secho("Indexing records...", fg='green')
        RecordIndexer().process_bulk_queue()
