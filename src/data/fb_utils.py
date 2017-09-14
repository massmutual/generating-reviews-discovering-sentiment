import argparse
import datetime
import sys
from collections import namedtuple

import ssl
import pymongo
import json

import urllib
import requests

FacebookConfig = namedtuple('FacebookConfig', 'access_token, id, start_date, url, name')

class InsightStore(object):
    def __init__(self, host='ttflx10026.private.massmutual.com', port=27017):
        self.client = pymongo.MongoClient(host,port)
        self.db = self.client.insights
    
    def get_most_recent(self, id, insight):
        collection = self.db[insight]
        return collection.find_one({"id": id}, sort=[('date', pymongo.DESCENDING)])

    def request_control(self, p_id):
        ret = True
        today = datetime.datetime.today().date()
        collection = self.db['posts']
        post = collection.find_one({'_id':p_id})
        if post != None:
            post_day = datetime.datetime.strptime(post['date'],'%Y-%m-%d').date()
            if (today-post_day).days > 30:
                ret = False
            if len(post.keys()) < 17: #even if post is > 30 days old, if it does not have all of the keys we need, make the requests
                ret = True
        return ret
    
    def save(self, insight, doc):
        collection = self.db[insight]
        id = collection.save(doc)

def create_insights_request(obj, metric, url, access_token, period=None):
    url = "/".join((url,obj,"insights",metric))
    vals = {"access_token":access_token}
    if period != None: 
        vals["period"] = period
    #request = urllib2.Request("?".join((url,urllib.urlencode(vals))))
    return (url, vals)


def create_page_request(url, access_token):
    vals = {"access_token":access_token}
    request = urllib2.Request("?".join((url,urllib.urlencode(vals))))
    return request

    
def get_insight(obj, metric, url, access_token, period=None):
    gcontext = ssl._create_unverified_context()
    request = create_insights_request(obj,metric,url,access_token)
    r = requests.get(request[0],params=request[1],verify=False)
    return r.json()


def parse_response(response, period):
    for p in response['data']:
        if p['period'] == period:
            return p['values']


def run(store, insight, fb_config, period=None):
    if insight == 'page_fans':
        period = 'lifetime'
    else:
        period = 'day'
    c = store.get_most_recent(fb_config.id, insight)
    if c != None:
        prev_date = datetime.datetime.strptime(c['date'], '%Y-%m-%d').date()
    else:
        prev_date = fb_config.start_date
    caught_up = False
    response = get_insight(fb_config.id, insight, fb_config.url, fb_config.access_token)
    print(fb_config.name)
    while not caught_up:
        records = parse_response(response, period)
        if records is None:
            caught_up = True
        else:
            for rec in records:
                if rec['value'] is not None:
                    if isinstance(rec['value'], dict):
                        r = dict([[k.replace(".","_"),v] for k,v in rec['value'].iteritems()])
                    else:
                        r = rec['value']
                    day = str(datetime.datetime.strptime(rec['end_time'].split('T')[0], '%Y-%m-%d').date() - datetime.timedelta(1))
                    store.save(insight, {'id':fb_config.id, 'date':day, 'value':r, 'name':fb_config.name, '_id':fb_config.name + day})
                    print('saved')
                    d = datetime.datetime.strptime(day, '%Y-%m-%d').date()
                    if d <= prev_date:
                        caught_up = True
            if not caught_up:
                response = requests.get(response["paging"]["previous"],verify=False).json()


