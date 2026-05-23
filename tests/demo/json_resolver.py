# SPDX-FileCopyrightText: 2016-2022 CERN.
# SPDX-License-Identifier: MIT

"""Test JSON resolver."""

import jsonresolver


@jsonresolver.route("/<path:item>", host="dx.doi.org")
def test_resolver(item):
    """Create a nested JSON."""
    return {"data": item}
