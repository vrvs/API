import json

class Hash:

    def __init__(self, name = "hash"):
        self._hash = {}
        self._name = name

    def _merge(self, ls1, ls2):
        ls = []
        count1 = 0
        count2 = 0
        len1 = len(ls1)
        len2 = len(ls2)
        while True:
            if count1 >= len1:
                ls.extend(ls2[count2:])
                break
            if count2 >= len2:
                ls.extend(ls1[count1:])
                break
            if ls1[count1] < ls2[count2]:
                ls.append(ls1[count1])
                count1 += 1
            elif ls1[count1] > ls2[count2]:
                ls.append(ls2[count2])
                count2 += 1
            else:
                ls.append(ls1[count1])
                count1 += 1
                count2 += 1
        return ls
    
    def load(self):
        path = 'untagged/indexer/datasets/hash/' + self._name + '.json'
        try:
            with open(path, 'r') as fileIn:
                self._hash = json.load(fileIn)
                fileIn.close()
        except IOError:
            with open(path, 'w') as fileOut:
                json.dump(self._hash, fileOut)
                fileOut.close()
    
    def save(self):
        path = 'untagged/indexer/datasets/hash/' + self._name + '.json'
        with open(path, 'w') as fileOut:
            json.dump(self._hash, fileOut)
            fileOut.close()
    
    def select(self, query, unique = False):
        refs = map(self.search, query)
        answer = []
        for ref in refs:
            answer = self._merge(answer, ref)
        if unique:
            for ref in refs:
                answer = filter(lambda x : x in ref, answer)
        return answer

    def insert(self, key, value):
        ls1 = self._hash.setdefault(key, [])
        if not isinstance(value, list):
            value = [value]
        st = set(value)
        ls2 = list(st)
        ls2.sort()
        newls = self._merge(ls1, ls2)
        self._hash[key] = newls

    def search(self, key):
        ls = self._hash.get(key, [])
        return ls

    def remove(self, key):
        try:
            del self._hash[key]
        except KeyError:
            pass

    def update(self, key, value):
        st = set(value)
        ls = list(st)
        ls.sort()
        self._hash[key] = ls
    
    def exist(self, key):
        test = self._hash.has_key(key)
        return test

    def compare(self, dictionary):
        test = cmp(self._hash, dictionary)
        return test

    def length(self):
        lng = len(self._hash)
        return lng

    def clear(self):
        self._hash.clear()

    def printable(self):
        s = str(self._hash)
        return s
        
    def copy(self):
        cp = self._hash.copy()
        return cp
        
    def itens(self):
        ls = self._hash.items()
        return ls
        
    def keys(self):
        k = self._hash.keys()
        return k
    
    def values(self):
        v = self._hash.values()
        return v
    
    def name(self):
        name = self._name
        return name
