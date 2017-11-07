import math

# function that returns the tdidf weight of a document
def weightFileTDIDF(word, text, invertedFile, fileTotalNumber, fileRecoveredNumber):
    tf = len(invertedFile["invertedFile"].get(word,[]))/float(invertedFile["size"])
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

# examples to test functions' correctness

word1 = "cat"
word2 = "bad"
text = "cat is so cute. cat is bad."
#       012345678901234567890123456
invertedFile = {"size": 4, "invertedFile": {"bad":[23],"cat":[0,16],"cute":[10]}}
fileTotalNumber = 200
fileRecoveredNumber = 50

query = ["cat","bad","cat","bad"]

text2 = "cat is so cute. cat is sad."
invertedFile2 = {"size": 4, "invertedFile": {"cat":[0,16],"cute":[10],"sad":[23]}}


print (weightFileTDIDF(word1,text,invertedFile,fileTotalNumber,fileRecoveredNumber))
print (weightFileTDIDF(word2,text,invertedFile,fileTotalNumber,fileRecoveredNumber))
print (vectorFile(query,text,invertedFile,fileTotalNumber,fileRecoveredNumber))
print (weightFileTDIDF(word1,text2,invertedFile2,fileTotalNumber,fileRecoveredNumber))
print (weightFileTDIDF(word2,text2,invertedFile2,fileTotalNumber,fileRecoveredNumber))
print (vectorFile(query,text2,invertedFile2,fileTotalNumber,fileRecoveredNumber))
print (vectorQuery(query,fileTotalNumber,fileRecoveredNumber))