import importlib

_stem = None

def load(algo = 'potter2'):
    global _stem
    if(algo == 'lovins'):
        from lexer.algorithms import lovins
        try: importlib.reload(lovins)
        except AttributeError: reload(lovins)
        _stem = lovins.stem
    elif(algo == 'paicehusk'):
        from lexer.algorithms import paicehusk
        try: importlib.reload(paicehusk)
        except AttributeError: reload(paicehusk)
        _stem = paicehusk.stem
    elif(algo == 'porter'):
        from lexer.algorithms import porter
        try: importlib.reload(porter)
        except AttributeError: reload(porter)
        _stem = porter.stem
    else:
        from lexer.algorithms import porter2
        try: importlib.reload(porter2)
        except AttributeError: reload(porter2)
        _stem = porter2.stem

def stemize(word):
    return _stem(word)