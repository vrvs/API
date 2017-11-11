import json


_ls = []
_la = []

def load(word):
    c = word[0]
    path = "untagged/lexer/thesaurus/thesaurus_update/" + c + ".json"
    with open(path, 'r') as fileIn:
        syn = json.load(fileIn)
        fileIn.close()
    return syn

def synonyms(word):
    global _ls
    _ls = []
    
    syn = load(word)
    dWord = syn.get(word)
    if dWord is not None:
        ctxKeys = dWord.keys()
        relev = 3
        while relev > 0:
            for key in ctxKeys:
                dCtx = dWord.get(key)
                if isinstance(dCtx,dict):
                    dSyn = dCtx.get("synonyms")
                    if dSyn.has_key(str(relev)):
                        _ls.extend(dSyn.get(str(relev)))
                else:
                    _ls.extend(synonyms(dCtx.encode("utf-8")))
                    relev = 0
            relev -= 1
    
    return _ls


def antonyms(word):
    global _la
    _la = []
    
    syn = load(word)
    dWord = syn.get(word)
    if dWord is not None:
        ctxKeys = dWord.keys()
        relev = 3
        while relev > 0:
            for key in ctxKeys:
                dCtx = dWord.get(key)
                if isinstance(dCtx,dict):
                    dSyn = dCtx.get("antonyms")
                    if dSyn.has_key(str(relev)):
                        _la.extend(dSyn.get(str(relev)))
                else:
                    _la.extend(antonyms(dCtx.encode("utf-8")))
                    relev = 0
            relev -= 1
    
    return _la