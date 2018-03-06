from app import Basic
import json

with open('sample.json') as json_data:
    docs = json.load(json_data)


# Why not int?
for doc in docs:
    basic = Basic(nconst = doc['nconst'], primaryName = doc['primaryName'], birthYear = str(doc['birthYear']), deathYear = str(doc['deathYear']), primaryProfession = doc['primaryProfession'], knownForTitles = doc['knownForTitles'])
    basic.save()
