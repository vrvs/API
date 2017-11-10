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
    
#function that return the size of the vector 
def norma (vector): 
    result = []
    norma = 0.0
    norma = [x**2 for x in vector]
    norma = sum(norma)
    norma = math.sqrt(norma)
    return norma

#function that return the correspondent vector that has the norma equals to 1
def normalize(vector):
    result = []
    normal = 0.0
    normal = norma(vector)
    result = [x/normal for x in vector]
    return result

#function that gives the similareties between the query and the documents that use as base the cossine 
def similarities (query, documents):
    result = []
    result = [cossine(query, x) for x in documents]
    return result
    

lista1 = [1,2]
lista4 = [2,-1]
lista2 = [2,3]
lista3 = [3,4]
lista5 = [lista2, lista3, lista4]
print(cossine(lista1, lista4))
print(similarities(lista1, lista5))
#ANALISAR DISSMILIDARIDADES ENRE OBJETOS