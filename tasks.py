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
from whoosh.index import open_dir

import urllib2
import json

def index_search():
    """
    Index OpdenFDA for searching.


    """
    root = test = os.path.dirname(os.path.realpath('__file__'))
    schema = Schema(name=TEXT(stored=True), category=ID(stored=True))
    ix = create_in(root+"/data/", schema)
    writer = ix.writer()
    
    dailymed_url = "http://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.json?pagesize=100&page=1"
    while(True):
        if dailymed_url != "null":
            response = urllib2.urlopen(dailymed_url)
            jdata = json.load(response)
            dailymed_url = jdata["metadata"]["next_page_url"]
            drugs = jdata["data"]
            for drug in drugs:
                 writer.add_document(name=unicode(drug["drug_name"]), category=unicode(drug["name_type"]))
        else:
            break
    writer.commit()


if __name__ == '__main__':
    append_index()

    