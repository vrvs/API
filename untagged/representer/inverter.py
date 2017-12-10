import json

class InvertedFile:
    
    def __init__(self, name = "inverded"):
        self._inverteds = {}
        self._name = name

    def load(self):
        path = 'untagged/representer/datasets/invertedFile/' + self._name + '.json'
        try:
            with open(path, 'r') as fileIn:
                self._inverteds = json.load(fileIn)
                fileIn.close()
        except IOError:
            with open(path, 'w') as fileOut:
                json.dump(self._inverteds, fileOut)
                fileOut.close()
    
    def save(self):
        path = 'untagged/representer/datasets/invertedFile/' + self._name + '.json'
        with open(path, 'w') as fileOut:
            json.dump(self._inverteds, fileOut)
            fileOut.close()
    
    def insert(self, key, fl):
        voc = set(fl)
        size = len(fl)
        result = {}
        for q in voc:
            result.setdefault(q, [])
            for i in range(size):
                if q == fl[i]:
                    result[q].append(i)
        self._inverteds[key] = result
        return result
    
    def search(self, key):
        ls = self._inverteds.get(key, [])
        return ls
    
    def select(self, keys):
        ls = map(self.search, keys)
        return ls
        
    def keys(self):
        ks = self._inverteds.keys()
        return ks
    
    def length(self):
        lng = len(self._inverteds)
        return lng

"""
# function that returns the tdidf weight of a document
def weightFileTDIDF(word, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    tf = len(invertedFile["invertedFile"].get(word,[]))/float(invertedFile["size"])
    idf = math.log(fileTotalNumber/fileRecoveredNumber,10);
    tfidf = tf*idf
    return tfidf

# function that returns the tdidf weight of a query
def weightQueryTDIDF(word, query, fileTotalNumber, fileRecoveredNumber):
    tf = query.count(word)/float(len(query))
    idf = math.log(fileTotalNumber/fileRecoveredNumber,10);
    tfidf = tf*idf
    return tfidf

# function that returns a vector of a document based on a query 
# a query with duplicate elements will remove the duplicates to build the vector
# example query = ["cat","bad","cat","bad"] will return a vector with two elements like [0.30102999566398114, 0.15051499783199057]
# because the second "cat" and the second "bad" will be eliminated
def vectorFile(query, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    result = []
    query = removeDuplicates(query)
    for q in query:
        result.append(weightFileTDIDF(q, text, invertedFile, fileTotalNumber, fileRecoveredNumber))
    return result
    
# function that returns a vector of a query
# a query with duplicate elements will remove the duplicates to build the vector
# example query = ["cat","bad","cat","bad"] will return a vector with two elements like [0.30102999566398114, 0.30102999566398114]
# because the second "cat" and the second "bad" will be eliminated  
def vectorQuery(query, fileTotalNumber, fileRecoveredNumber):
    result = []
    queryM = removeDuplicates(query)
    for q in queryM:
        result.append(weightQueryTDIDF(q, query, fileTotalNumber, fileRecoveredNumber))
    return result


#this function recives a vector 
#return the vector divided by its norm
def cossine (document, query):
    result = 0.0
    normalizedDoc = normalize(document)
    normalizedQuery = normalize(query)
    for i in range (2):
        result += normalizedDoc[i]*normalizedQuery[i]
    return result
    
# function that return the size of the vector 
def norma (vector): 
    result = []
    norma = 0.0
    norma = [x**2 for x in vector]
    norma = sum(norma)
    norma = math.sqrt(norma)
    return norma

# function that return the correspondent vector that has the norma equals to 1
def normalize(vector):
    result = []
    normal = 0.0
    normal = norma(vector)
    result = [x/normal for x in vector]
    return result

# function that gives the similareties between the query and the documents using the cossine as base 
def similarities (query, documents):
    result = []
    result = [cossine(query, x) for x in documents]
    return result
"""
