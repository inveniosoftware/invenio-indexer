Full text indexer
=================

The branch ``sprint-full-text-indexersprint-full-text-indexer`` is used to show an example of full
text indexer for elasticsearch, or how to index the whole text of each documents, no matter its
format (text, CSV, HTML, PDF...).

1. Installation
---------------

In order to use this feature, you need to install some additional
packages.

1.1. additional dependency to invenio-records-files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As it indexes the files inside a record, you need to install the package invenio-records-files:

::

    pip install invenio-records-files

1.2. Mapper Attachment plugin for elasticsearch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Then, you need to install the mapper attachment plugin for elasticsearch, in order to improve the
elasticsearch capabilities and be able to index the text inside the documents.

For more information about this plugin, see
https://www.elastic.co/guide/en/elasticsearch/plugins/current/mapper-attachments.html

This plugin runs with Tika, so it is able to extract text content from several file format. See
http://lucene.apache.org/tika/

To install it, you need to run the ``plugin`` command from elasticsearch.

Depending on your OS and your elasticsearch installation, it is located in different places.

For Linux:

::

    sudo /bin/plugin install mapper-attachments

For OSX:

::

    /usr/local/Cellar/elasticsearch/2.4.1/libexec/bin/plugin install mapper-attachments

2. Usage
--------

In order to run the example, you need to run the following commands:

::

    cd examples
    ./app-setup.sh
    ./app-fixtures.sh
    FLASK_APP=app.py flask run

Then, you'll be able to query elasticsearch on
``localhost:9200/testrecords-testrecord-v1.0.0/_search``. Here you can look at the indexed text.

The example files are located in ``examples/files``.
