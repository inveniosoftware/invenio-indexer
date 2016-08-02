#!/bin/sh

pip install invenio-db
[ -e "app.db" ] && rm app.db
export FLASK_APP=app.py
flask db init
flask db create
flask index destroy --yes-i-know
flask index init
flask index queue init
flask fixtures records
flask index reindex --yes-i-know
flask index run
