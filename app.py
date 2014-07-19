#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
app
--------------

Main Flask app for the `searchfda` module.

"""
import sys
import urllib
import re
import urllib2
import json
import time
import functools
import os
from collections import namedtuple
from datetime import datetime, time, timedelta

from flask import Flask, request, session, render_template, jsonify, redirect
from flask.ext.sqlalchemy import SQLAlchemy
import requests
from pyquery import PyQuery
import pytz

import flask
import utils
import settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///search.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


#Home page
@app.route("/")
def home():

    return render_template("home.html", test="test")


#Search page
@app.route('/search=<search>/', strict_slashes=False)
def search(search):
    search_results = utils.fetch_search(search)
    #flask.jsonify(search_results)
    return render_template('search.html',searchterm=search, searchresults=search_results)


#Result page
@app.route('/search=<search>/<category>/<view>', strict_slashes=False)
def results(search, category, view):
    description = utils.fetch_description(search)
    adverse_events = utils.fetch_adverse_events(search,category,view)
    recalls = utils.fetch_recalls(search)
    return render_template('results.html', description=description, adverse_events=adverse_events, recalls=recalls)


if __name__ == '__main__':
    
    if '-c' in sys.argv:
        create_data()
    else:
        app.run(debug=True, port=65010)
