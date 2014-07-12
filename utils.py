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
    #if category == generic_name:
        #if view = histogram
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
        #else: #time    
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
    #elif category == manufactuter_name:
        #if view = histogram
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
        #else: #time    
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
    #elif category == reactionmeddrapt:
        #if view = histogram
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
        #else: #time    
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
    #elif category == indication:
        #if view = histogram
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
        #else: #time    
            #openfda_url = "https://api.fda.gov/drug/event.json?search=" + "___" + "&count=" + "___"
    #else:
        #return error
    openfda_url = "https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:Sumatriptan&count=patient.drug.drugindication&limit=30"
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH&"
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)
    results = [{"key":"blah","values":jdata["results"]}]

    return results

    
    
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

