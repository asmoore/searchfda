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
from math import ceil

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
@app.route("/", methods=['GET'])
def home():
    autocomplete = [{"result":"CSS"},{"result":"JavaScript"},{"result":"Java"},{"result":"Ruby"},{"result":"PHP"}]
    search_results = utils.fetch_search("sumatriptan",1)
    return render_template("home.html", autocomplete=autocomplete, searchresults=search_results)


#Autocomplete
@app.route('/autocomplete', methods=['POST'])
def autocomplete():
    data = request.data
    search_results = utils.fetch_search(data)
    return search_results[0]["name"]
    #return search_results


#Search page
#@app.route('/search=<search>/', strict_slashes=False)
@app.route('/search=<search>/', defaults={'page': 1})
@app.route('/search=<search>/page/<int:page>')
def search(search,page):
    (search_results, total) = utils.fetch_search(search,page)
    pagination = Pagination(page, 10, total)
    print pagination
    return render_template('search.html',searchterm=search, searchresults=search_results, pagination=pagination, currentpage=page)


#Result page
@app.route('/search=<search>/result/', strict_slashes=False)
def results(search):
    description = utils.fetch_description(search)
    adverse_events = utils.fetch_adverse_events(search,category,view)
    recalls = utils.fetch_recalls(search)
    return render_template('results.html', description=description, adverse_events=adverse_events, recalls=recalls)


#Recalls page
@app.route('/search=<search>/result/recall/')
def recall(search):
    recalls = utils.fetch_recalls(search)
    keys = recalls[0].keys()
    values = recalls[0].values()
    return render_template('recall.html', recalls=recalls[0])


#Adverse events page
@app.route('/search=<search>/result/adverse/')
def adverse(search):
    adverse_events = utils.fetch_adverse_events(search,"G","indication")
    keys = adverse_events[0].keys()
    values = adverse_events[0].values()
    return render_template('recall.html',recalls=adverse_events[0])


#Labels page
@app.route('/search=<search>/result/label/')
def label(search):
    labels = utils.fetch_labels(search)
    keys = labels[0].keys()
    values = labels[0].values()
    return render_template('label.html', labels=labels[0])


class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


if __name__ == '__main__':
    
    if '-c' in sys.argv:
        create_data()
    else:
        app.run(debug=True, port=65010)

