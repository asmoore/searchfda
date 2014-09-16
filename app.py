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
    return render_template("home.html")


#Autocomplete
@app.route('/autocomplete')
def autocomplete():
    search_input = request.args.get('search_input',"None",type=str)
    search_results = utils.fetch_search(search_input,1)
    return jsonify(result=search_results[0])


#Search page
#@app.route('/search=<search>/', strict_slashes=False)
@app.route('/search=<search>/', defaults={'page': 1})
@app.route('/search=<search>/page/<int:page>')
def search(search,page):
    (search_results, total) = utils.fetch_search(search,page)
    pagination = Pagination(page, 10, total)
    return render_template('search.html',searchterm=search, searchresults=search_results, pagination=pagination, currentpage=page)


#Result page
@app.route('/result/count=<count>/search=<search>/report=<int:report>', strict_slashes=False)
def results(count,search,report):
    adverse_event_count = utils.fetch_adverse_event_count(search,count)
    (adverse_event, total_reports) = utils.fetch_adverse_event(search, report)
    pagination = Pagination(report, 1, total_reports)
    return render_template('result.html', 
        adverse_event_count=adverse_event_count, 
        adverse_event=adverse_event, 
        count=count, 
        search=search, 
        total_reports=total_reports,
        pagination=pagination,
        currentpage=report)
    

#Adverse page
@app.route('/adverse/<searchterm>/count=<count>/search=<search>/report=<int:report>', strict_slashes=False)
def adverse(searchterm,count,search,report):
    adverse_event_count = utils.fetch_adverse_event_count(search,count)
    (adverse_event, total_reports) = utils.fetch_adverse_event(search, report)
    pagination = Pagination(report, 1, total_reports)
    return render_template('adverse.html', 
        adverse_event_count=adverse_event_count, 
        adverse_event=adverse_event,
        searchterm=searchterm, 
        count=count, 
        search=search, 
        total_reports=total_reports,
        pagination=pagination,
        currentpage=report)


#recall page
@app.route('/recall/<searchterm>/count=<count>/search=<search>/report=<int:report>', strict_slashes=False)
def recall(searchterm,count,search,report):
    recall_count = utils.fetch_recall_count(search,count)
    return render_template('recall.html', 
        searchterm=searchterm, 
        count=count, 
        search=search, 
        currentpage=report,
        recall_count=recall_count)


#Label page
@app.route('/label/<searchterm>/count=<count>/search=<search>/report=<int:report>', strict_slashes=False)
def label(searchterm,count,search,report):
    (label, spl_set_id) = utils.fetch_label(search)
    media_url = utils.fetch_label_media(spl_set_id)
    return render_template('label.html', 
        searchterm=searchterm, 
        count=count, 
        search=search, 
        label=label,
        spl_set_id=spl_set_id,
        media_url=media_url)


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

