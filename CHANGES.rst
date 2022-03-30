..
    This file is part of Invenio.
    Copyright (C) 2016-2019 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 1.2.2 (released 2022-03-30)

- Add support for Click v8.1+ and Flask v2.1+.

Version 1.2.1 (released 2021-03-05)

- Remove pytest runner from setup dependencies

Version 1.2.0 (released 2020-09-16)

- Changes delete requests to optimistic concurrency control by providing the
  the version and version_type in delete requests. The previous behavior can
  restored by calling
  ``RecordIndexer().delete(record, version=None, version_type=None)`` instead.

- Adds support for using new-style record dumping controlled via the
  ``Record.enable_jsonref`` flag.

Version 1.1.2 (released 2020-04-28)

- Introduces ``RecordIndexer.record_cls`` for customizing the record class.
- Removes Python 2 support.

Version 1.1.1 (released 2019-11-21)

- Fix bulk action parameters compatibility for Elasticsearch v7.

Version 1.1.0 (released 2019-07-19)

- Add support for Elasticsearch v7.
- Integrate index prefixing.
- Add ``before_record_index.dynamic_connect()`` signal utility for more
  flexible indexer receivers.
- Add ``schema_to_index`` utility from ``invenio-search`` (will be removed in
  next minor version of ``invenio-search``).

Version 1.0.2 (released 2019-05-27)

- Allow Elasticsearch indexing arguments to be modified by subscribing to
  ``before_record_index`` signal.

Version 1.0.1 (released 2018-10-11)

- Allow forwarding arguments from ``RecordIndexer.process_bulk_queue`` to
  ``elasticsearch.helpers.bulk`` calls via the ``es_bulk_kwargs`` parameter.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
