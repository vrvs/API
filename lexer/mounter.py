import normalization as norm
import json

with open("stopwords/stopwords.txt", 'r') as fileIn:
    words = fileIn.read()
    fileIn.close()

words = norm.normalize(words)
words = norm.tokenize(words)
ds = set(words)
    
with open("stopwords/stopwords.json", 'w') as fileOut:
    json.dump(list(ds), fileOut)
    fileOut.close()
    