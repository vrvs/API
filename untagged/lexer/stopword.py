import json

_sw = set()

def load(path = "untagged/lexer/stopwords/stopwords.json"):
    global _sw
    with open(path, 'r') as fileIn:
        words = json.load(fileIn)
        _sw = set(words)
        fileIn.close()

def save(path = "untagged/lexer/stopwords/stopwords.json"):
    words = list(_sw)
    with open(path, 'w') as fileOut:
        json.dump(words, fileOut)
        fileOut.close()

def transform(query):
    func = lambda x : x not in _sw
    newQuery = filter(func, query)
    return newQuery

def contains(word):
    flag = word in _sw
    return flag

def words():
    ls = list(_sw)
    return ls

def size():
    size = len(_sw)
    return size

def insert(word):
    _sw.add(word)

def remove(word):
    _sw.discard(word)
    
def clear():
    _sw.clear()