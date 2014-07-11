#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tasks
--------------

Tasks functions for the `searchfda` module.

"""

from whoosh.index import create_in
from whoosh.fields import *

index_search():
    """
    Index OpdenFDA for searching.


    """

    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in("indexdir", schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a", content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
    content=u"The second one is even more interesting!")
    writer.commit()

