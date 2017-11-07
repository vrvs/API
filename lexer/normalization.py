def tokenize(text):
    tokens = text.split()
    return tokens

def normalize(text):
    # $, %, #, &, @
    chars = ['!', '"', '(', ')', '*', '+', ',', '-', '/', \
             ':', ';', '<', '=', '>', '?', '[', ']', '^', \
             '_', '`', '{', '|', '}', '~', '\\']
    for char in chars:
        text = text.replace(char, ' ')
    text = text.replace('.', '')
    text = text.replace("'", '')
    text = text.lower()
    return text

def lemmatize(text):
    print('Still not implemented, important to semantic analasys! ;-)')