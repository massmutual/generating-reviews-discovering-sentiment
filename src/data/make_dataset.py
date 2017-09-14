import urllib
import urllib2
import requests
import json
import argparse
import datetime
import sys
import ssl
from collections import namedtuple

from storage.storage import *


FacebookConfig = namedtuple('FacebookConfig', 'access_token, id, start_date, url, name')


args = parser.parse_args()
store = InsightStore()
insight_metrics = json.load(open('/home/mm64067/facebook/insights/util/insight_metrics.json'))
config = json.load(open('/home/mm64067/facebook/insights/config.json'))
#     insight_metrics = json.load(open('util/insight_metrics.json'))
#     config = json.load(open('config.json'))
print 'Getting Insights'
for page in config["id_list"]:
    mth,day,yr = map(int, page["date"].split("-"))
    start_date = datetime.date(yr,mth,day)
    fb_config = FacebookConfig._make([page['access_token'], page['id'], start_date, config['url'], page['name']])
    if args.all:
        arg = []
        for metric in ["stories","page_impressions","engagement","demographics","content","views","domain_content"]:
            for i in insight_metrics[metric]:
                arg.append("--"+i)
                if i == 'page_fans':
                    print 'page_fans'
        args = parser.parse_args(arg)

    if args.page_impressions:
        run(store, 'page_impressions', fb_config)