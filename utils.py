#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
utils
--------------

Utility functions for the `searchfda` module.

"""
from collections import namedtuple
import urllib2
import json
from datetime import datetime, time, timedelta, date
import re
import os

import praw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm
from whoosh.index import open_dir
from whoosh.fields import *

import app
import settings

def fetch_search(search):
    """
    Fetch search results.

    """
    jsondata = """
{"name":Sumatriptan", "category":"generic drug name"},
{"name": "Imitrex", "category":"brand name"}
"""
    search_results = []
    root = test = os.path.dirname(os.path.realpath('__file__'))
    ix = open_dir(root+"/data/")
    with ix.searcher() as searcher:
        query = QueryParser("name", ix.schema, termclass=FuzzyTerm).parse(search)
        results = searcher.search(query)
        for hit in results[0:5]:
            search_results.append({"name": hit["name"],"category": hit["category"], "view":"indication"})
    
    return search_results
    
    
def fetch_results(search,category,view):
    """
    Fetch search results.

    """


    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    if category == "B":
        search = "patient.drug.openfda.brand_name:"+search
    else:
        search = "patient.drug.openfda.generic_name:"+search
    count = "patient.drug.drugindication.exact"
    openfda_url = ''.join(["https://api.fda.gov/drug/event.json?",
        "api_key=",api_key,
        "&search=",search,
        "&count=",count,
        "&limit=30"])
    print openfda_url
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)

    return jdata["results"]

    
    
def fetch_drugevent_json(search,count):
    """
    Fetch json data from OpenFDA.

    """
    #openfda_url = "https://api.fda.gov/drug/event.json?search=receivedate:[20040101+TO+20150101]&count=receivedate"
    
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH&"
    search = "receivedate:[20040101+TO+20150101]"
    count = "receivedate"
    openfda_url = ("https://api.fda.gov/drug/event.json?",
        "api_key=",api_key,
        "&search=",search,
        "&count=",count)
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)

    return jdata
    

if __name__ == '__main__':
    #engine = create_engine('sqlite:///games.db')
    #engine = create_engine(os.environ['DATABASE_URL'])
    Session = sessionmaker(bind=engine)    
    session = Session()
    session._model_changes = {}

