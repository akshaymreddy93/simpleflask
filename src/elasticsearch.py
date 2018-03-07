# from elasticsearch import Elasticsearch
from app import Basic
#import simplejson as json
import json


# es = Elasticsearch()


# data = json.loads(open('companies.json').read())
# print(data)

with open('companies.json') as f:
        for line in f:
            print(line.encode('ascii', 'ignore').decode('utf-8'))
