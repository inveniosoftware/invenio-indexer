#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Always bring down docker services
function cleanup() {
    eval "$(docker-services-cli down --env)"
}
trap cleanup EXIT


python -m check_manifest --ignore ".*-requirements.txt"
python -m sphinx.cmd.build -qnNW docs docs/_build/html
eval "$(docker-services-cli up --search ${SEARCH:-elasticsearch} --cache ${CACHE:-redis} --mq ${MQ:-rabbitmq} --env)"
if [ "${SEARCH}" = "opensearch2" ]; then
    curl -XPUT localhost:9200/_cluster/settings -H "Content-Type:application/json" -d "{\"persistent\": {\"compatibility\": {\"override_main_response_version\": \"true\"}}}"
fi
if [ "${SEARCH}" = "opensearch1" ]; then
    curl -XPUT localhost:9200/_cluster/settings -H "Content-Type:application/json" -d "{\"persistent\": {\"compatibility\": {\"override_main_response_version\": \"true\"}}}"
fi
python -m pytest
tests_exit_code=$?
exit "$tests_exit_code"
