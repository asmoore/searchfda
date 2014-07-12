#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tasks
--------------

Tasks functions for the `searchfda` module.

"""

import os

from whoosh.index import create_in
from whoosh.fields import *

def index_search():
    """
    Index OpdenFDA for searching.


    """
    root = test = os.path.dirname(os.path.realpath('__file__'))
    schema = Schema(name=TEXT(stored=True), category=ID(stored=True), type=TEXT)
    ix = create_in(root+"/data/", schema)
    writer = ix.writer()
    writer.add_document(name=u"Sumatriptan", category=u"generic", type=u"adverse event")
    writer.add_document(name=u"Sumatriptan Succinate", category=u"generic",type=u"adverse event")
    writer.commit()


if __name__ == '__main__':
    index_search()