..
    SPDX-FileCopyrightText: 2016-2018 CERN.
    SPDX-License-Identifier: MIT

Installation
============

Invenio-Indexer is on PyPI so all you need is:

.. code-block:: console

   $ pip install invenio-indexer

Invenio-Indexer depends on Invenio-Search, Invenio-Records and Celery/Kombu.

**Requirements**

Invenio-Indexer requires a message queue in addition to the search engine
(Invenio-Search) and the database (Invenio-Records). See Kombu documentation
for list of supported message queues (e.g. RabbitMQ):
http://kombu.readthedocs.io/en/latest/introduction.html#transport-comparison
