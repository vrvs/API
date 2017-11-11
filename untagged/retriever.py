import os
from ranker import *
from representer import *
from indexer import *
from lexer import *

_container = None

def init(name = None, stemAlgo = None, stopDict = None, orthoDict = None):
    global _container
    if stemAlgo is not None:
        stemming.load(stemAlgo)
    else:
        stemming.load()
    if stopDict is not None:
        stopword.load(stopDict)
    else:
        stopword.load()
    if orthoDict is not None:
        orthography.load(orthoDict)
    else:
        orthography.load()
    if name is not None:
        _container = hashing.Hash(name)
        _container.load()
        
def _transform(query):
    query = normalization.normalize(query)
    query = normalization.tokenize(query)
    query = orthography.transform(query)
    query = stopword.transform(query)
    query = stemming.transform(query)
    return query
    
def indexContainer(parentKey, comments):
    global _container
    for key in comments.keys():
        indexContent(parentKey, key, comments[key])
    _container.save()
    
def indexContent(parentKey, key, comment):
    comment = _transform(comment)
    name = _container.name() + "Contents/"
    newpath = 'untagged/indexer/datasets/hash/' + name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    content = hashing.Hash(name + str(parentKey))
    content.load()
    for token in comment:
        content.insert(token, key)
        _container.insert(token, parentKey)
    content.save()
    newpath = 'untagged/representer/datasets/invertedFile/' + name
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    inverted = inverter.InvertedFile(name + str(parentKey))
    inverted.load()
    inverted.insert(key, comment)
    inverted.save()
    
'''
def retrieveContainer(query, filters = []):
    query = _transform(query)
    elements = _container.select(query)
    filters = set(filters)
    elements = filter(lambda x : x in filters, elements)
    files = {}
    for element in elements:
        name = _container.name() + "Contents/"
        content = hash.Hash(name + str(parentKey))
        content.load()
        files[element] = 
    '''
tComments = {"UR123797508": "I was looking for a place to sleep nearby the airport. I didn't care too much about amenities or decor. But hey, the place is full of drug addicts. Used condoms in the stairway. I ran away from this place as fast as I could.",\
             "UR2778933": "This nasty Motel 6 is in a high crime area and is run down. The check in staff was rude and unhelpful. Drug dealers and hookers everywhere on the streets. Bedding was dirty with stains and burn holes, was woke up several times in the night by people partying in the apartment complex next door, then woke up at 5am by the garbage truck. Gave up trying to sleep and Left.",\
             "UR24501030": "We expected Motel 6 to be basic but we were not prepared for the awfulness of this one. The room appeared very dirty and the bed linen - if it had been changed - was full of holes and stained. I feel sorry for the Motel 6s which try - we have stayed in some- but the brand is totally trashed by experiences such as this one. We will be avoiding all Motel 6s in future."}

tKey = "73869"

init("hotels")
indexContainer(tKey, tComments)