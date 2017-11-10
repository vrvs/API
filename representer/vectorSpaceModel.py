import math
#import sys
#sys.path.insert(0, "/workspace/ranker")
#import ranker
#from ranker import ranking 

# function that returns a vector of a document based on a query 
# a query with duplicate elements will remove the duplicates to build the vector
# example query = ["cat","bad","cat","bad"] will return a vector with two elements like [0.30102999566398114, 0.15051499783199057]
# because the second "cat" and the second "bad" will be eliminated
def vectorFile(query, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    result = []
 #   query = ranking.removeDuplicates(query)
    #for q in query:
  #      result.append(ranking.weightFileTDIDF(q, text, invertedFile, fileTotalNumber, fileRecoveredNumber))
   # return result
    
# function that returns a vector of a query
# a query with duplicate elements will remove the duplicates to build the vector
# example query = ["cat","bad","cat","bad"] will return a vector with two elements like [0.30102999566398114, 0.30102999566398114]
# because the second "cat" and the second "bad" will be eliminated  
def vectorQuery(query, fileTotalNumber, fileRecoveredNumber):
    result = []
#    queryM = ranking.removeDuplicates(query)
 #   for q in queryM:
 #       result.append(ranking.weightQueryTDIDF(q, query, fileTotalNumber, fileRecoveredNumber))
 #   return result


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
    
def invertedFile (file):
    result = {}
    vocabulary = []
    posicion = []
    voc = []
    size = 0
    vocabulary = file.split()
    voc = removeDuplicates(vocabulary)
    size = len(vocabulary)
    for q in voc:
        result[q] = []
    for q in voc:
        for i in range(size):
            if q == vocabulary[i]:
                result[q].append(i)
     
    return result
    
def removeDuplicates(query):
    result = []
    for q in query:
       if q not in result:
           result.append(q)
    return result
    
#lista1 = [1,2]
#lista4 = [2,-1]
#lista2 = [2,3]
#lista3 = [3,4]
#lista5 = [lista2, lista3, lista4]
#print(cossine(lista1, lista4))
#print(similarities(lista1, lista5))
print(invertedFile("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."))

#ANALISAR DISSMILIDARIDADES ENRE OBJETOS