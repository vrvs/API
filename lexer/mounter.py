import json

ls = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'x', 'w', 'y', 'z']

for carac in ls:

    with open("lexer/thesaurus/"+carac+".json", 'r') as fileIn:
        thesaurus = json.load(fileIn)
        fileIn.close()

    aux = {}
    aux1 = {}
    aux2 = {}
    aux3 = {}
    aux4 = {}

    keysWords= thesaurus.keys()
    
    for key in keysWords:
        dictWord = thesaurus.get(key)
        ctxKeys = dictWord.keys()
        
        for key1 in ctxKeys:
            if isinstance(dictWord, dict):
                dictCtx = dictWord.get(key1)
        
                if isinstance(dictCtx, dict): 
                    ctxKeys = dictCtx.keys()
                    
                    for key2 in ctxKeys:
                        synonyms = dictCtx[key2]
                        synonymsKeys = synonyms.keys()
            
                        for key3 in synonymsKeys:
                            i = synonyms.get(key3)
                            aux4.setdefault(i, [])
                            aux4[i].append(key3)
                        aux3.update({key2:aux4})
                        aux4 = {}
                        synonyms.clear()
                    #print aux2
                    aux2.update({key1:aux3})
                    aux3 = {}
                    dictCtx.clear()
                else:
                    aux2.update({key1:dictCtx})
        aux1.update({key:aux2})
        aux2 = {}
        dictWord.clear()
                
    with open("lexer/thesaurus/thesaurus_update/"+carac+".json", 'w') as fileOut:
        json.dump(aux1, fileOut)
        fileOut.close()
