# system
import sys
import os
from dotenv import find_dotenv, load_dotenv
# dataset / api access
import ssl
import pymongo
import json
import urllib
import requests
# misc
import argparse
import datetime
from collections import namedtuple
# local
from fb_utils import InsightStore

# load secrets
dotenv_success = load_dotenv(find_dotenv())
if not dotenv_success:
    print("dotenv not loaded")

print(os.environ.get("user"))

# accessing mongo
client = pymongo.MongoClient('')
db = client['']
collection = db['']



FacebookConfig = namedtuple('FacebookConfig', 'access_token, id, start_date, url, name')
store = InsightStore()

insight_metrics = json.load(open('./insight_metrics.json'))
config = json.load(open('./config.json'))

page = config["id_list"][1]
mth,day,yr = map(int, page["date"].split("-"))
start_date = datetime.date(yr,mth,day)

fb_config = FacebookConfig._make([page['access_token'], page['id'], start_date, config['url'], page['name']])




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
                    print('page_fans')
        args = parser.parse_args(arg)

    if args.page_impressions:
        run(store, 'page_impressions', fb_config)