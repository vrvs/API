# encoding: utf-8
import json

_sw = {}

def load(path = "stopwords/stopwords.json"):
    with open(path, 'r') as fileIn:
        _sw = json.load(fileIn)
        fileIn.close()
    return _sw

def save(path = "stopwords/stopwords.json"):
    with open(path, 'w') as fileOut:
        json.dump(_sw, fileOut)
        fileOut.close()

def contains(word):
    
    