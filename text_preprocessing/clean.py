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



