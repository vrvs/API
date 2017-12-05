""" \package Normalization
Module responsible for preprocessing requisitions to perform standardization, 
tokenization and lemmatization of search strings.
"""

def tokenize(text):
    """
    Stop character-based tokenization function (' ', \\n, \\t, \\r, \\f) 
    receives as input a query and returns a list of chains representing search 
    tokens.
    \param text String - query to be tokenized
    \return list - list of string tokenized
    """
    tokens = text.split()
    return tokens

def normalize(text):
    """
    Function responsible for performing standardization of the search string, 
    removing irrelevant character in the search, such as: interrogation, 
    exclamation, dot, apostrophes, ...
    \param text String - query to be normalized
    \return String - normalized text
    """
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
    """
    Method for obtaining semantic characteristics, performs conversion of 
    characteristic terms, such as: Aren't to be, I'm to I am.
    \param text String - query to be lemmatized
    """
    print('Still not implemented, important to semantic analasys! ;-)')