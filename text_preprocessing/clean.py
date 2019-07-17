# General imports
import numpy as np
import pandas as pd
import os, sys, gc, re, warnings, pickle, itertools, emoji, psutil, random, unicodedata

# custom imports
from gensim.utils import deaccent
from collections import Counter
from bs4 import BeautifulSoup
from multiprocessing import Pool

warnings.filterwarnings('ignore')
pd.options.display.max_columns = 10
pd.options.display.max_colwidth = 200

### Initial State
verbose = True
global_lower=True

WPLACEHOLDER = 'word_placeholder'

def _check_replace(w):
    return not bool(re.search(WPLACEHOLDER, w))

def _make_cleaning(s, c_dict):
    if _check_replace(s):
        s = s.translate(c_dict)
    return s

def _check_vocab(c_list, vocabulary, response='default'):
    try:
        words = set([w for line in c_list for w in line.split()])
        print('Total Words :',len(words))
        u_list = words.difference(set(vocabulary))
        k_list = words.difference(u_list)
    
        if response=='default':
            print('Unknown words:', len(u_list), '| Known words:', len(k_list))
        elif response=='unknown_list':
            return list(u_list)
        elif response=='known_list':
            return list(k_list)
    except:
        return []
    
def _make_dict_cleaning(s, w_dict):
    if _check_replace(s):
        s = w_dict.get(s, s)
    return s

def _print_dict(temp_dict, n_items=10):
    run = 0
    for k,v in temp_dict.items():
        print(k,'---',v)
        run +=1
        if run==n_items:
            break  


#################### Main Function #################

def to_lower(data):
    if verbose: print('#'*10 ,'Step - Lowering everything:')
    data = list(map(lambda x: x.lower(), data))
    return data

def to_normalize(data):
    if verbose: print('#'*10 ,'Step - Normalize chars and dots:')

    normalized_chars = {}
    
    chars = '‒–―‐—━—-▬'
    for char in chars:
        normalized_chars[ord(char)] = '-'

    chars = '«»“”¨"'
    for char in chars:
        normalized_chars[ord(char)] = '"'

    chars = "’'ʻˈ´`′‘’\x92"
    for char in chars:
        normalized_chars[ord(char)] = "'"

    chars = '̲_'
    for char in chars:
        normalized_chars[ord(char)] = '_'

    chars = '\xad\x7f'
    for char in chars:
        normalized_chars[ord(char)] = ''

    chars = '\n\r\t\u200b\x96'
    for char in chars:
        normalized_chars[ord(char)] = ' '

    # Normalize chars and dots - SEE HELPER FOR DETAILS
    # Global
    data = list(map(lambda x: ' '.join([_make_cleaning(i,normalized_chars) for i in x.split()]), data))
    data = list(map(lambda x: re.sub('\(dot\)', '.', x), data))
    data = list(map(lambda x: deaccent(x), data))
    
    return data

def remove_control_char(data):
    if verbose: print('#'*10 ,'Step - Control Chars:')
    global_chars_list = list(set([c for line in data for c in line]))
    chars_dict = {c:'' for c in global_chars_list if unicodedata.category(c)[0]=='C'}
    data = list(map(lambda x: ' '.join([_make_cleaning(i,chars_dict) for i in x.split()]), data))
    
    return data

def remove_href(data):
    if verbose: print('#'*10 ,'Step - Remove hrefs:')
    data = list(map(lambda x: re.sub(re.findall(r'\<a(.*?)\>', x)[0], '', x) if (len(re.findall(r'\<a (.*?)\>', x))>0) and ('href' in re.findall(r'\<a (.*?)\>', x)[0]) else x, data))
    return data

def remove_duplicate(data):
    # Duplicated dots, question marks and exclamations
    # Locallocal_vocab
    if verbose: print('#' * 10, 'Step - Duplicated Chars:')
    local_vocab={}
    temp_vocab = _check_vocab(data, local_vocab, response='unknown_list')
    temp_vocab = [k for k in temp_vocab if _check_replace(k)]
    temp_dict = {}
    
    for word in temp_vocab:
        new_word = word
        if (Counter(word)['.']>1) or (Counter(word)['!']>1) or (Counter(word)['?']>1) or (Counter(word)[',']>1):
            if (Counter(word)['.']>1):
                new_word = re.sub('\.\.+', ' . . . ', new_word)
            if (Counter(word)['!']>1):
                new_word = re.sub('\!\!+', ' ! ! ! ', new_word)
            if (Counter(word)['?']>1):
                new_word = re.sub('\?\?+', ' ? ? ? ', new_word)
            if (Counter(word)[',']>1):
                new_word = re.sub('\,\,+', ' , , , ', new_word)
            temp_dict[word] = new_word
            
    temp_dict = {k: v for k, v in temp_dict.items() if k != v}
    data = list(map(lambda x: ' '.join([_make_dict_cleaning(i,temp_dict) for i in x.split()]), data))
    return data

