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

def fetch_openfda():
    """
    Fetch json data from OpenFDA.

    """
    test = "test"

    return test

    
if __name__ == '__main__':
    #engine = create_engine('sqlite:///games.db')
    #engine = create_engine(os.environ['DATABASE_URL'])
    Session = sessionmaker(bind=engine)    
    session = Session()
    session._model_changes = {}

