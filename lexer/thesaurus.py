""" \package Thesaurus
Module responsible for getting synonyms and antonyms of a especific word
"""

import json

def _removeDuplicates(l):
    """
    function that, given a list l, returns all elements of the list without 
    duplicated elements
    \param l list - list of tokenized strings
    \return list - list of tokenized strings without duplications
    """
    result = []
    for q in l:
       if q not in result:
           result.append(q)
    return result

def _load(word):
    """
    function that, given a word, loads the corresponding file (json)
    in thesaurus directory which is named with the first letter of 
    the word, and returns a dictionary that represents it
    \param word String - keyword to be searched in thesaurus
    \return dict - a dictionary that represents de begin letter of the word
    """
    c = word[0]
    path = "lexer/thesaurus/thesaurus_update/" + c + ".json"
    with open(path, 'r') as fileIn:
        syn = json.load(fileIn)
        fileIn.close()
    return syn

def synonyms(word):
    """
    function that, given a word, searches in the dictionary and returns the
    list of synonyms of the word with no duplicate elements
    \param word String - keyword to be searched in the dictionary returned by the load
    \return list - a list with all synonyms of the word without duplicates
    """
    ls = []
    
    syn = _load(word)
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
                        ls.extend(dSyn.get(str(relev)))
                else:
                    ls.extend(synonyms(dCtx.encode("utf-8")))
                    relev = 0
            relev -= 1
    
    return _removeDuplicates(ls)


def antonyms(word):
    """
    function that, given a word, searches in the dictionary and returns the
    list of antonyms of the word with no duplicate elements
    \param word String - keyword to be searched in the dictionary returned by the load
    \return list - a list with all antonyms of the word without duplicates
    """
    
    la = []
    
    syn = _load(word)
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
                        la.extend(dSyn.get(str(relev)))
                else:
                    la.extend(antonyms(dCtx.encode("utf-8")))
                    relev = 0
            relev -= 1
    
    return _removeDuplicates(la)
