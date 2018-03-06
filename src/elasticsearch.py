from elasticsearch import Elasticsearch
from app import Basic
#import simplejson as json
import json


es = Elasticsearch()

for obj in Basic.objects:
    print(obj.primaryName)

#s = json.dumps(Basic())
#print(s)
