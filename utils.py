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
from pyquery import PyQuery

import praw
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm
from whoosh.index import open_dir
from whoosh.fields import *

import app
import settings

def fetch_search(search,page):
    """
    Fetch search results.

    """
    search_results = []
    root = test = os.path.dirname(os.path.realpath('__file__'))
    ix = open_dir(root+"/data/")
    with ix.searcher() as searcher:
        query = QueryParser("name", ix.schema, termclass=FuzzyTerm).parse(search)
        results = searcher.search_page(query,page,10)
        total = results.total
        print total
        for hit in results:
            if hit["category"] == "B":
                category = "Brand name drug"
            elif hit["category"] == "G":
                category = "Generic drug"
            else:
                category = hit["category"]
            search_results.append({"name": hit["name"].capitalize(),"category": category, "view":"indication"})
    #total = 2
    return (search_results,total)
    
    
def fetch_adverse_events(search,category,view):
    """
    Fetch adverse events from OpenFDA.

    """
    limit="20";
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
        "&limit=",limit])
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)

    return jdata["results"]


def fetch_recalls(search):
    """
    Fetch recalls from OpenFDA.

    """
    limit="1";
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    search = "openfda.substance_name:"
    count = "openfda.manufacturer_name.exact"
    openfda_url = ''.join(["https://api.fda.gov/drug/enforcement.json?",
        "api_key=",api_key,
        "&search=",search,
        "&count=",count,
        "&limit=",limit])
    openfda_url = "https://api.fda.gov/drug/enforcement.json?search=report_date:[20040101+TO+20131231]&limit=1"
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)

    return jdata["results"]


def fetch_labels(search):
    """
    Fetch labels from OpenFDA.

    """
    labels="nothing";
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    search = "openfda.substance_name:"
    count = "openfda.manufacturer_name.exact"
    openfda_url = ''.join(["https://api.fda.gov/drug/enforcement.json?",
        "api_key=",api_key,
        "&search=",search,
        "&count=",count,
        "&limit=",limit])
    openfda_url = "https://api.fda.gov/drug/enforcement.json?search=report_date:[20040101+TO+20131231]&limit=1"
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)

    return jdata["results"]


def fetch_description(search):
    """
    fetch description from MedlinePlus

    """
    medline_url = "http://apps.nlm.nih.gov/medlineplus/services/mpconnect_service.cfm?mainSearchCriteria.v.cs=2.16.840.1.113883.6.88&mainSearchCriteria.v.dn="+search+"&informationRecipient.languageCode.c=en&knowledgeResponseType=application/json"
    response = urllib2.urlopen(medline_url)
    jdata = json.load(response)
    description_url = jdata["feed"]["entry"][0]["link"][0]["href"]    
    pq = PyQuery(description_url)
    description = pq("p")[0].text

    return description    

    
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

