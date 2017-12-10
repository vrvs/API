import math
import sys
import itertools

def weightFileTDIDF(word, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    """
    function that returns the tdidf weight of a document
    \param word String - keyword to produce a weight relationed to it
    \param text String - tokenized search string (query)
    \param invertedFile dict - inverted file related to the comment
    \param fileTotalNumber int - number of comments
    \param fileRecoveredNumber int - number of retrieved comments
    \return double - weight related to the word
    """
    tf = len(invertedFile.get(word,[]))/float(size(invertedFile))
    idf = math.log(fileTotalNumber/fileRecoveredNumber,10);
    tfidf = tf*idf
    return tfidf

def size(invertedFile):
    """
    function that calculates the number of words in a document (inverted file)
    \param invertedFile dict - inverted file related to the comment
    \return int - size of the inverted file
    """
    values = invertedFile.values()
    length = map(lambda x: len(x), values)
    length = sum(length)
    return length


def vectorFile(query, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    """
    function that returns a vector of a document based on a query.
    a query with duplicate elements will remove the duplicates to build the vector
    example query = ["cat","bad","cat","bad"] will return a vector with two elements like [0.30102999566398114, 0.15051499783199057]
    because the second "cat" and the second "bad" will be eliminated
    \param query list - list of words that represents the search string 
    \param text String - tokenized search string (query)
    \param invertedFile dict - inverted file related to the comment
    \param fileTotalNumber int - number of comments
    \param fileRecoveredNumber int - number of retrieved comments
    \return list - list that represents a vector
    """
    result = []
    query = removeDuplicates(query)
    for q in query:
        result.append(weightFileTDIDF(q, text, invertedFile, fileTotalNumber, fileRecoveredNumber))
    return result
 
# function that returns the tdidf weight of a query
def weightQueryTDIDF(word, query, fileTotalNumber, fileRecoveredNumber):
    tf = query.count(word)/float(len(query))
    idf = math.log(fileTotalNumber/fileRecoveredNumber,10);
    tfidf = tf*idf
    return tfidf

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
    
# function that eliminate the duplicates of a query
def removeDuplicates(query):
    result = []
    for q in query:
       if q not in result:
           result.append(q)
    return result

# function that calculates the cossine between two vectors
# It was did because I needed to use Vector Space Model to do my tests
def cos(vector1, vector2):
    l = range(0,len(vector1))
    num = 0
    for i in l:
        num += (vector1[i] * vector2[i])
    vector1 = map(lambda x: x ** 2, vector1)
    vector2 = map(lambda x: x ** 2, vector2)
    x1 = sum(vector1)
    x2 = sum(vector2)
    x1 = math.sqrt(x1)
    x2 = math.sqrt(x2)
    den = x1*x2
    if den == 0:
        return 0
    return num/den

###############################################################################
# here is a method using term proximity thought by Valdemiro. I didn't find any 
# place that do the same. Maybe there is but not sure
# Based in a method that uses Vector Space Model and Term Proximity and 
# calculates a matrix with distance between terms
# I thought that do the sum between this distances could be a nice heuristic
# that returns a good result (need to be validated by Lucas Rufino to be sure 
# that it returns a good result in a decent time)
# It is important say that here uses Vector Space Model to calculate the relecance too,
# when the weight of term proximity is the same

# function that calculates the minimun distance between two terms in a doc
def minDist(term1, term2, invertedFile):
    if len(invertedFile.get(term1,[])) == 0:
        return 15000
    if len(invertedFile.get(term2,[])) == 0:
        return 15000
    minValue = 15000
    list1 = invertedFile.get(term1)
    list2 = invertedFile.get(term2)
    l1 = range(0,len(list1))
    l2 = range(0,len(list2))
    for i in l1:
        for j in l2:
            if(list1[i]<list2[j]):
                if(list2[j]-(list1[i]+len(term1))<minValue):
                    minValue = list2[j]-(list1[i]+len(term1))
            else:
                if(list1[i]-(list2[j]+len(term2))<minValue):
                    minValue = list1[i]-(list2[j]+len(term2))
    return minValue

#function that calculates the minimum distance between all terms of the query
# and stores in a two-dimensional list
def matrixDist(query, invertedFile):
    query = removeDuplicates(query)
    matrix = [[0 for x in range(len(query))] for y in range(len(query))]
    l1 = range(0,len(query))
    for i in l1:
        for j in l1:
            if i!=j:
                matrix[i][j] = minDist(query[i],query[j],invertedFile)
    return matrix

#function that do the sum of all distances
def weightFileTermProximity(query, invertedFile):
    if(len(query)==1):
        l1 = invertedFile.get(query[0],[])
        if(len(l1)==0):
            return sys.float_info.max
        else:
            return 1/len(l1)
    return (float)(sum(map(sum, matrixDist(query, invertedFile)))/2)

#function that receive a query, a doc list, a inverted file list, the total
# number of all documents that exists in database, and the total number
# of files that were recovered and returns a pair list of weight and docs
# in relevance order
def rankingDocsaux(query, docs, invertedFiles, fileTotalNumber, pair):
    fileRecoveredNumber = len(docs)
    length =  range(0,len(docs))
    query = removeDuplicates(query)
    vecQuery = vectorQuery(query,fileTotalNumber, fileRecoveredNumber)
    for i in length:
        termProx = weightFileTermProximity(query, invertedFiles[i])
        vect = -(cos(vecQuery, vectorFile(query, docs[i], invertedFiles[i],fileTotalNumber, fileRecoveredNumber)))
        aux = pair[i][3]
        if pair[i][0]>termProx:
            pair[i] = [termProx, vect, docs[i], blocks(query, invertedFiles[i])]
        elif (pair[i][0]==termProx) and (pair[i][1]>vect):
            pair[i] = [termProx, vect, docs[i], blocks(query, invertedFiles[i])]
    pair = sorted(pair)
    return pair

def rankingContainers1aux(query, dictionary,pair):
    entity = dictionary.keys()
    size = []
    comments = []
    invertedFiles = []
    for e in entity:
        size.append(dictionary[e]["fileTotalNumber"])
        aux = dictionary[e]["comments"].keys()
        comments.append(aux)
        aux2 = []
        for a in aux:
            aux2.append(dictionary[e]["comments"][a])
        invertedFiles.append(aux2)
    length =  range(0,len(entity))
    for i in length:
        pair2 = [[999999999.0,0.0,docs[0],[]] for x in range(len(comments[i]))]
        aux = rankingDocsaux(query,comments[i],invertedFiles[i],dictionary[entity[i]]["fileTotalNumber"],pair2)
        aux2 = [0.0,0.0,entity[0],"",[]]
        for a in min(range(0,5),range(0,len(aux))):
            aux2[0] += aux[a][0]
            aux2[1] += aux[a][1]
        aux2[0] /= min(5,len(aux))
        aux2[1] /= min(5,len(aux))
        aux2[2] = entity[i]
        aux2[3] = aux[0][2]
        aux2[4] = aux[0][3]
        if(pair[i][0]>aux2[0]):
            pair[i] = aux[0]
        elif (pair[i][0]==aux2[0]) and (pair[i][1]>aux2[1]):
            pair[i] = aux[0]
    pair = sorted(pair)
    return pair



def rankingDocs(querys, docs, invertedFiles, fileTotalNumber):
    querys = [p for p in itertools.product(*querys)]
    pair = [[999999999.0,0.0,docs[0],[]] for x in range(len(docs))]
    for q in querys:
        pair = rankingDocsaux(q, docs, invertedFiles, fileTotalNumber, pair)
    return pair

def rankingContainers1(querys, dictionary):
    querys = [p for p in itertools.product(*querys)]
    entity = dictionary.keys()
    pair = [[0.0,0.0,entity[0],"",[]] for x in range(len(entity))]
    for q in querys:
        pair = rankingContainers1aux(q, dictionary,pair)
    return pair
    
    

def blocks(query, invertedFile):
    l = invertedFile.keys()
    block = {}
    for i in l:
        ls = invertedFile[i]
        t = range(0,len(ls))
        for j in t:
            if block.get(abs(ls[j]),None) == None:
                block[abs(ls[j])] = 0
    for q in query:
        if q[0] == '-':
            aux = q[1:len(q)]
            l = invertedFile.get(aux,[])
            l = list(filter(lambda x: x < 0, l))
        else:
            l = invertedFile.get(q,[])
            l = list(filter(lambda x: x > 0, l))
        for i in l:
            block[abs(i)] = block[abs(i)] + 1
    l = block.keys()
    a = []
    for b in l:
        a.append([block[b],b])
    a = sorted(a)
    a = reversed(a)
    a = list(a)
    b = []
    for t in a:
        b.append(t[1])
    return b


querys = [["w","-b","-l"],["d"],["-f","a"]]
docs = ["a w b, h. a", "a y. u v", "r. t b, f", "d t, b a"]
invertedFile = [ { "a":[1,-3],"b":[-1],"w":[1],"h":[-2] }, { "a":[1],"y":[1],"u":[2],"v":[-2]  }, { "d":[-1],"t":[-1],"b":[2],"a":[2] } ]
print(blocks(querys[0],invertedFile[0]))
fileTotalNumber = 1000



#############################################################################
# This method is more reliable because we get this from a book of information
# retrieval area (Information Retrieval: Implementing and Evaluating Search Engines) 
# It uses the idea of covering. We define a cover as a window that contains all
# elements from the query. A cover can't contain a cover in itself. 
# The key of the algorithm is calculate all covers avaliable in a doc
# and uses the window values(all of them) to calculate the score of the file
# Then, we rank the docs based in these scores
# Here, we use, again, the Vector Space Model as second priority


# function that returns a list with all elements of the query that is in the doc
def getList(query,invertedFile):
    query = removeDuplicates(query)
    result = []
    for q in query:
        l1 = map(lambda x: [x,q], invertedFile.get(q,[]))
        for l in l1:
            result.append(l)
    result = sorted(result)
    return result

# function that calculate all covers of a doc based in a query
def allCovers(query,invertedFile):
    i = 0
    j = 0
    l1 = getList(query, invertedFile)
    result = []
    query = removeDuplicates(query)
    elements = []
    s = range(j,len(l1))
    for k in s:
        elements.append(l1[k][1])
        if isCovered(elements,query):
            while isCovered(elements,query):
                elements.remove(l1[i][1])
                i += 1
            i -= 1
            elements.append(l1[i][1])
            if(isCovered(elements,query)):
                result.append([l1[i][0],l1[k][0]])
            elements.remove(l1[i][1])
            i += 1
    return result


# function that says if a window is a cover
# I know that It may not to seen so efficient but It is what I could do
def isCovered(elements,query):
    elements = removeDuplicates(elements)
    query = sorted(query)
    elements = sorted(elements)
    return query == elements
    
# function that calculates a score of a document based on a query    
def score(query, invertedFile):
    l1 = allCovers(query,invertedFile)
    result = 0.0
    for l in l1:
        result += 1.0/(l[1]-l[0]+1)
    return result
    
#function that receive a query, a doc list, a inverted file list, the total
# number of all documents that exists in database, and the total number
# of files that were recovered and returns a pair list of weight and docs
# in relevance order
def rankingFiles(query, docs, invertedFiles, fileTotalNumber):
    fileRecoveredNumber = len(docs)
    pair = [[0,0.0,docs[0]] for x in range(len(docs))]
    length = range(0,len(docs))
    vecQuery = vectorQuery(query,fileTotalNumber, fileRecoveredNumber)
    for i in length:
        pair[i] = [score(query,invertedFiles[i]), cos(vecQuery, vectorFile(query, docs[i], invertedFiles[i],fileTotalNumber, fileRecoveredNumber)) , docs[i]]
    pair = sorted(pair,reverse=True)
    return pair

def rankingContainers(query, dictionary):
    entity = dictionary.keys()
    size = []
    comments = []
    invertedFiles = []
    for e in entity:
        size.append(dictionary[e]["fileTotalNumber"])
        aux = dictionary[e]["comments"].keys()
        comments.append(aux)
        aux2 = []
        for a in aux:
            aux2.append(dictionary[e]["comments"][a])
        invertedFiles.append(aux2)
    pair = [[0,0.0,0.0,entity[0]] for x in range(len(entity))]
    length =  range(0,len(entity))
    for i in length:
        aux = rankingFiles(query,comments[i],invertedFiles[i],dictionary[entity[i]]["fileTotalNumber"])
        aux2 = len(filter(lambda x: x[0] > 0.0, aux))
        if aux2 == 0:
            aux2 = sys.maxsize
        pair[i][0] = -aux2
        for a in min(range(0,5),range(0,len(aux))):
            pair[i][1] += aux[a][0]
            pair[i][2] += aux[a][1]
        aux1 = pair[i][1] / min(5,len(aux))
        aux2 = pair[i][2] / min(5,len(aux))
        pair[i][1] += aux1*(5-min(5,len(aux)))
        pair[i][2] += aux2*(5-min(5,len(aux)))
        pair[i][3] = entity[i]
    pair = sorted(pair)
    return pair
