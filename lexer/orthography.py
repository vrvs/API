import json

_ortho = set()

def load(path = "lexer/dictionaries/alphanumeric.json"):
    global _ortho
    with open(path, 'r') as fileIn:
        words = json.load(fileIn)
        _ortho = set(words)
        fileIn.close()

def save(path = "lexer/dictionaries/alphanumeric.json"):
    words = list(_ortho)
    with open(path, 'w') as fileOut:
        json.dump(words, fileOut)
        fileOut.close()

def convert(query):
    func = lambda x : x not in _ortho
    newQuery = filter(func, query)
    return newQuery

def contains(word):
    flag = word in _ortho
    return flag

def words():
    ls = list(_ortho)
    return ls

def size():
    size = len(_ortho)
    return size

def insert(word):
    _ortho.add(word)

def remove(word):
    _ortho.discard(word)
    
def clear():
    _ortho.clear()