from en_core_web_sm import load
import tqdm
import numpy as np


nlp = load()

pos_dict={'VERB': 0,
  'NOUN': 1,
  'ADP': 2,
  'SCONJ': 3,
  'SYM': 4,
  'CCONJ': 5,
  'SPACE': 6,
  'X': 7,
  'PUNCT': 8,
  'INTJ': 9,
  'PROPN': 10,
  'ADV': 11,
  'AUX': 12,
  'ADJ': 13,
  'DET': 14,
  'NUM': 15,
  'PRON': 16,
  'PART': 17}

tag_dict={'VBN': 0,
  'RBR': 1,
  'EX': 2,
  '_SP': 3,
  'VBD': 4,
  'NN': 5,
  'SYM': 6,
  'RBS': 7,
  ':': 8,
  'NNS': 9,
  'WP$': 10,
  'UH': 11,
  'JJR': 12,
  '-RRB-': 13,
  'CC': 14,
  'VBZ': 15,
  'TO': 16,
  'PRP$': 17,
  ',': 18,
  'JJ': 19,
  '-LRB-': 20,
  'RB': 21,
  'NNP': 22,
  'DT': 23,
  'RP': 24,
  'VBG': 25,
  "''": 26,
  'WDT': 27,
  'MD': 28,
  'FW': 29,
  'CD': 30,
  'PRP': 31,
  'JJS': 32,
  'VB': 33,
  'WP': 34,
  'LS': 35,
  'XX': 36,
  'AFX': 37,
  'WRB': 38,
  'HYPH': 39,
  'POS': 40,
  'VBP': 41,
  'NFP': 42,
  '``': 43,
  'NNPS': 44,
  'PDT': 45,
  '.': 46,
  'IN': 47}

dep_dict={'nsubj': 0,
  '': 1,
  'advcl': 2,
  'prep': 3,
  'relcl': 4,
  'intj': 5,
  'ccomp': 6,
  'amod': 7,
  'appos': 8,
  'prt': 9,
  'nmod': 10,
  'aux': 11,
  'xcomp': 12,
  'csubjpass': 13,
  'case': 14,
  'pobj': 15,
  'oprd': 16,
  'nummod': 17,
  'punct': 18,
  'compound': 19,
  'attr': 20,
  'advmod': 21,
  'meta': 22,
  'poss': 23,
  'parataxis': 24,
  'dative': 25,
  'cc': 26,
  'acomp': 27,
  'neg': 28,
  'dobj': 29,
  'agent': 30,
  'quantmod': 31,
  'det': 32,
  'auxpass': 33,
  'mark': 34,
  'pcomp': 35,
  'expl': 36,
  'nsubjpass': 37,
  'npadvmod': 38,
  'acl': 39,
  'conj': 40,
  'predet': 41,
  'csubj': 42,
  'dep': 43,
  'preconj': 44,
  'ROOT': 45}

def add_padding(tokens, max_len):
    
    if len(tokens)==max_len:
        return tokens
    elif len(tokens) > max_len:
        return tokens[0:max_len]
    else:
        while(len(tokens)<max_len):
            tokens.append(0)
        return tokens

def get_tokens(text):
    doc = nlp(text)
    final_token_1 = []
    final_token_2 = []
    final_token_3 = []
    for token in doc:
        final_token_1.append(pos_dict[token.pos_])
        final_token_2.append(tag_dict[token.tag_])
        final_token_3.append(dep_dict[token.dep_])
    #print('len :', len(final_token))
    return final_token_1, final_token_2, final_token_3

def get_tokens_plus(texts, max_seq_length=120):
    tokens1 = []
    tokens2 = []
    tokens3 = []
    for i in tqdm.tqdm(range(len(texts))):
        text = texts[i]
        tok1,tok2, tok3 = get_tokens(text)
        tok1 = add_padding(tok1, max_seq_length)
        tok2 = add_padding(tok2, max_seq_length)
        tok2 = add_padding(tok3, max_seq_length)
        tokens1.append(tok1)
        tokens2.append(tok2)
        tokens3.append(tok3)
        
    return np.array(tokens1), np.array(tokens2), np.array(tokens3)