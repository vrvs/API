# encoding: utf-8

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