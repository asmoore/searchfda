#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tasks
--------------

Tasks functions for the `searchfda` module.

"""

import os
import time
import urllib2
import json

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir

import utils

def index_search():
    """
    Index OpdenFDA for searching.


    """
    root = test = os.path.dirname(os.path.realpath('__file__'))
    schema = Schema(name=TEXT(stored=True), category=ID(stored=True),ae_number=TEXT(stored=True),recall_number=TEXT(stored=True))
    ix = create_in(root+"/data/", schema)
    writer = ix.writer()
    
    dailymed_url = "http://dailymed.nlm.nih.gov/dailymed/services/v2/drugnames.json?pagesize=100&page=1"
    
    while(True):
        if dailymed_url != "null":
            try:
                response = urllib2.urlopen(dailymed_url)
                jdata = json.load(response)
                dailymed_url = jdata["metadata"]["next_page_url"]
                print dailymed_url
                drugs = jdata["data"]
                for drug in drugs:
                    recall_number = utils.get_recall_number(str(drug["drug_name"]))
                    ae_number = utils.get_ae_number(str(drug["drug_name"]))
                    writer.add_document(name=unicode(drug["drug_name"]), 
                                        category=unicode(drug["name_type"]), 
                                        ae_number=unicode(ae_number), 
                                        recall_number=unicode(recall_number))
            except:
                print "couldn't load " + dailymed_url
        else:
            break
        time.sleep(60)
    writer.commit()

def index_search2():
    root = test = os.path.dirname(os.path.realpath('__file__'))
    schema = Schema(name=TEXT(stored=True), category=ID(stored=True))
    ix = create_in(root+"/data/", schema)
    writer = ix.writer()
    drug_name = "sumatriptan"
    
    #Get number of recalls for drug
    recall_url = 'https://api.fda.gov/drug/enforcement.json?search=openfda.substance_name:"'+drug_name+'"&limit=1'
    response = urllib2.urlopen(recall_url)
    jdata = json.load(response)
    recall_number = jdata["meta"]["results"]["total"]
    print "recalls: " + str(recall_number) + "\n"

    ae_url = 'https://api.fda.gov/drug/event.json?search=patient.drug.openfda.substance_name:"'+drug_name+'"&limit=1'
    response = urllib2.urlopen(ae_url)
    jdata = json.load(response)
    ae_number = jdata["meta"]["results"]["total"]
    print "Adverse events: " + str(ae_number) + "\n"


def index_OpenFDA(startNumber):
    """
    Append OpenFDA quantities to Whoosh index

    """
    root = test = os.path.dirname(os.path.realpath('__file__'))
    ix = open_dir(root+"/data/")
    reader = ix.reader()

    #OpenFDA 240/minute limit
    #OpenFDA 120,000/day limit
    for i in range(startNumber,(startNumber+10)):
        result = reader.stored_fields(i)
        
        print result["name"]
        ae_number = utils.get_ae_number(result["name"])
        print ae_number

        recall_number = utils.get_recall_number(result["name"])
        print recall_number
    
    print i


if __name__ == '__main__':
    index_search()
    #append_index()

    