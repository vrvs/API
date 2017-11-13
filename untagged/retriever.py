from ranker import *
from representer import *
from indexer import *
from lexer import *
import threading
import os

class Th(threading.Thread):
    
    def __init__(self, query, keys):
        threading.Thread.__init__(self)
        self._query = query
        self._keys = keys
        self._rank = []
        
    def run(self):
        files = {}
        name = _container.name() + "Contents/"
        for key in self._keys:
            content = hashing.Hash(name + str(key))
            inverted = inverter.InvertedFile(name + str(key))
            content.load()
            inverted.load()
            
            element = files.setdefault(key, {})
            element['fileTotalNumber'] = inverted.length()
            comments = element.setdefault("comments", {})
            refs = content.select(self._query)
            for ref in refs:
                comments[ref] = inverted.search(ref)
        for key in files.keys():
            if files[key]['comments'] == {}:
                del files[key]
        if not files == {}:
            self._rank = ranking.rankingContainers1(self._query, files)
    
    def ranking(self):
        return self._rank
        

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
    else:
        _container = hashing.Hash()

def load():
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
    content = hashing.Hash(_container.name() + "Contents/" + str(parentKey))
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
    
def retrieveContainer(query, filters = []):
    query = _transform(query)
    if filters == []:
        filters = _container.select(query)
    
    count = 0
    filtersTh = [ [] for _ in range(16)]
    for key in filters:
        filtersTh[count].append(key)
        count += 1
        if(count == 16):
            count = 0
    
    threads = []
    for i in range(16):
        threads.append(Th(query, filtersTh[i]))
        threads[-1].start()
    
    rank = []
    for th in threads:
        th.join()
        rank.extend(th.ranking())
    rank.sort()
    rank = map(lambda x : x[2], rank)
    rankSet = set(rank)
    concat = filter(lambda x : x not in rankSet, filters)
    rank.extend(concat)
    return rank
    
def retrieveContent(query, key, filters = []):
    name = _container.name() + "Contents/"
    content = hashing.Hash(name + str(key))
    inverted = inverter.InvertedFile(name + str(key))
    content.load()
    inverted.load()
    
    query = _transform(query)
    docs = content.select(query)
    invertedFiles = inverted.select(docs)
    fileTotalNumber = inverted.length()
    rank = []
    if not invertedFiles == []:
        rank = ranking.rankingDocs(query, docs, invertedFiles, fileTotalNumber)
    rank = map(lambda x : x[2], rank)
    rankSet = set(rank)
    if not filters == []:
        concat = filter(lambda x : x not in rankSet, filters)
    else:
        concat = filter(lambda x : x not in rankSet, inverted.keys())
    rank.extend(concat)
    return rank