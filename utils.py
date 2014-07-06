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

import app
import settings

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
    response = urllib2.urlopen(nba_url)
    jdata = json.load(response)

    return jdata
    
        
if __name__ == '__main__':
    #engine = create_engine('sqlite:///games.db')
    #engine = create_engine(os.environ['DATABASE_URL'])
    Session = sessionmaker(bind=engine)    
    session = Session()
    session._model_changes = {}

