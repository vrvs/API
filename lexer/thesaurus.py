# encoding: utf-8
import json


_ls = set()

def load(word):
    c = word[0]
    path = "lexer/thesaurus/" + c + ".json"
    with open(path, 'r') as fileIn:
        syn = json.load(fileIn)
        fileIn.close()
    return syn

def synonyms(word):
    global _ls
    _ls.clear()
    
    syn = load(word)
    ctxKeys = syn.get(word)
    keys = ctxKeys.keys()
    relevance = 3
    
    for key in keys:
        synoms = ctxKeys.get(key)
        lsyn = synoms.get("synonyms")
        synKeys = lsyn.keys()
        
        while relevance:
            for key1 in synKeys:
                if lsyn.get(key1) == relevance:
                    _ls.add(key1)
            
            if len(_ls) > 0:
                relevance = 0
            else:
                relevance = relevance-1
    
    return _ls