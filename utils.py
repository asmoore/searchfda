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
            print hit
            if hit["category"] == "B":
                category = "Brand name drug"
            elif hit["category"] == "G":
                category = "Generic drug"
            else:
                category = hit["category"]
            search_results.append({"name": hit["name"].capitalize(),
                                   "category": category,
                                   "adverse": hit["adverse"],
                                   "recall": hit["recall"],
                                   "label": hit["label"]})
    #total = 2
    return (search_results,total)
    
    
def fetch_adverse_event_count(search,count):
    """
    Fetch adverse event counts from OpenFDA.

    """
    limit="20"
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    openfda_url = ''.join(["https://api.fda.gov/drug/event.json?",
        "api_key=",api_key,
        "&search=",search,
        "&count=",count,
        "&limit=",limit])
    
    openfda_url = openfda_url.replace(" ","%20")
    openfda_url = openfda_url.replace('"',"%22")
    print openfda_url
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)

    return jdata["results"]


def fetch_adverse_event(search,report):
    """
    Fetch adverse events from OpenFDA.

    """
    limit="1"
    skip=str(int(report)-1)
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    openfda_url = ''.join(["https://api.fda.gov/drug/event.json?",
        "api_key=",api_key,
        "&search=",search,
        "&limit=",limit,
        "&skip=",skip])
    
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)
    results = jdata["results"]
    total_reports = jdata["meta"]["results"]["total"]
    return (results, total_reports)


def fetch_recall_count(search, count):
    """
    Fetch recalls from OpenFDA.

    """
    limit="20"
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    openfda_url = ''.join(["https://api.fda.gov/drug/enforcement.json?",
        "api_key=",api_key,
        "&search=",search,
        "&count=",count,
        "&limit=",limit])
    
    openfda_url = openfda_url.replace(" ","%20")
    openfda_url = openfda_url.replace('"',"%22")
    print openfda_url
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)

    return jdata["results"]


def fetch_label(search):
    """
    Fetch label from OpenFDA.

    """
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    limit = "1"
    openfda_url = ''.join(["https://api.fda.gov/drug/label.json?",
        "api_key=",api_key,
        "&search=",search,
        "&limit=",limit])
    response = urllib2.urlopen(openfda_url)
    jdata = json.load(response)
    spl_set_id = jdata["results"][0]["openfda"]["spl_set_id"][0]

    return (jdata["results"], spl_set_id)


def fetch_label_media(spl_id):
    """
    Fetch label media from Dailymed

    """
    dailymed_url = ''.join(["http://dailymed.nlm.nih.gov/dailymed/services/v2/spls/",
        spl_id,
        "/media.json"])
    response = urllib2.urlopen(dailymed_url)
    jdata = json.load(response)
    media_url = jdata["data"]["media"]
    return media_url

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

    
def get_ae_number(drug_name):
    """
    Get number of adverse events for drug 

    """
    limit="1";
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    drug_name = drug_name.replace(" ","%20")
    search = 'patient.drug.medicinalproduct:"'+drug_name+'"'
    openfda_url = ''.join(["https://api.fda.gov/drug/event.json?",
        "api_key=",api_key,
        "&search=",search,
        "&limit=",limit])

    try:
        response = urllib2.urlopen(openfda_url)
        jdata = json.load(response)
        count = jdata['meta']['results']['total']
    except:
        count = 0
    #indication = jdata['results'][0]['term'] 
    return count   

def get_recall_number(drug_name):
    """
    Get number of recalls
    
    """
    limit="1";
    api_key = "QxCHqxHE1kHDwbBFj2WRh3w8y3aepivT42vgCQDH"
    drug_name = drug_name.replace(" ","%20")
    search = 'openfda.substance_name:"'+drug_name+'"'
    openfda_url = ''.join(["https://api.fda.gov/drug/enforcement.json?",
        "api_key=",api_key,
        "&search=",search,
        "&limit=",limit])
    try:
        response = urllib2.urlopen(openfda_url)
        jdata = json.load(response)
        count = jdata['meta']['results']['total']
    except:
        count = 0
    return count


if __name__ == '__main__':
    #engine = create_engine('sqlite:///games.db')
    #engine = create_engine(os.environ['DATABASE_URL'])
    Session = sessionmaker(bind=engine)    
    session = Session()
    session._model_changes = {}

