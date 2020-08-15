import spacy
import numpy as np
from tqdm import tqdm

try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)", file=stderr)
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm', disable=['parser','ner','tagger'])
    nlp.vocab.add_flag(lambda s: s.lower() in spacy.lang.en.stop_words.STOP_WORDS, spacy.attrs.IS_STOP)


pos_dict={'[PAD]': 0,
 'VERB': 1,
 'NOUN': 2,
 'ADP': 3,
 'SCONJ': 4,
 'SYM': 5,
 'CCONJ': 6,
 'SPACE': 7,
 'X': 8,
 'PUNCT': 9,
 'INTJ': 10,
 'PROPN': 11,
 'ADV': 12,
 'AUX': 13,
 'ADJ': 14,
 'DET': 15,
 'NUM': 16,
 'PRON': 17,
 'PART': 18}

tag_dict={'[PAD]': 0,
 'VBN': 1,
 'RBR': 2,
 'EX': 3,
 '_SP': 4,
 'VBD': 5,
 'NN': 6,
 'SYM': 7,
 'RBS': 8,
 ':': 9,
 'NNS': 10,
 'WP$': 11,
 'UH': 12,
 'JJR': 13,
 '-RRB-': 14,
 'CC': 15,
 'VBZ': 16,
 'TO': 17,
 'PRP$': 18,
 ',': 19,
 'JJ': 20,
 '-LRB-': 21,
 'RB': 22,
 'NNP': 23,
 'DT': 24,
 'RP': 25,
 'VBG': 26,
 "''": 27,
 'WDT': 28,
 'MD': 29,
 'FW': 30,
 'CD': 31,
 'PRP': 32,
 'JJS': 33,
 'VB': 34,
 'WP': 35,
 'LS': 36,
 'XX': 37,
 'AFX': 38,
 'WRB': 39,
 'HYPH': 40,
 'POS': 41,
 'VBP': 42,
 'NFP': 43,
 '``': 44,
 'NNPS': 45,
 'PDT': 46,
 '.': 47,
 'IN': 48}


dep_dict={'[PAD]': 0,
 'nsubj': 1,
 '': 2,
 'advcl': 3,
 'prep': 4,
 'relcl': 5,
 'intj': 6,
 'ccomp': 7,
 'amod': 8,
 'appos': 9,
 'prt': 10,
 'nmod': 11,
 'aux': 12,
 'xcomp': 13,
 'csubjpass': 14,
 'case': 15,
 'pobj': 16,
 'oprd': 17,
 'nummod': 18,
 'punct': 19,
 'compound': 20,
 'attr': 21,
 'advmod': 22,
 'meta': 23,
 'poss': 24,
 'parataxis': 25,
 'dative': 26,
 'cc': 27,
 'acomp': 28,
 'neg': 29,
 'dobj': 30,
 'agent': 31,
 'quantmod': 32,
 'det': 33,
 'auxpass': 34,
 'mark': 35,
 'pcomp': 36,
 'expl': 37,
 'nsubjpass': 38,
 'npadvmod': 39,
 'acl': 40,
 'conj': 41,
 'predet': 42,
 'csubj': 43,
 'dep': 44,
 'preconj': 45,
 'ROOT': 46}

def convert_by_vocab(vocab, items):
  """Converts a sequence of [tokens|ids] using the vocab."""
  output = []
  for item in items:
    output.append(vocab[item])
  return output

class SpacyParseTokenizer():
    def __init__(self, parsers=['pos','tag','dep']):
        self.parsers = parsers
        self.pos_vocab = pos_dict
        self.inv_pos_vocab = {v: k for k, v in self.pos_vocab.items()}
        self.tag_vocab = tag_dict
        self.inv_tag_vocab = {v: k for k, v in self.tag_vocab.items()}
        self.dep_vocab = dep_dict
        self.inv_dep_vocab = {v: k for k, v in self.dep_vocab.items()}

    def __add_padding(self, tokens, max_seq):

        if len(tokens)==max_seq:
            return tokens
        elif len(tokens) > max_seq:
            return tokens[0:max_seq]
        else:
            while(len(tokens)<max_seq):
                tokens.append(0)
            return tokens

    def __call__(self, inputs, call_type='encode', max_seq=None):
        """`__call__` method allow a single interface to call encode, encode_plus and tokenize methods

        Args:

            inputs (List or string): It can be string (for encode call type) or List for encode_plus and tokenize

            call_type (str, optional): can be encode, encode_plus, tokenize. Defaults to 'encode'.

            max_seq ([type], optional): it applies for encode and encode_plus call_type Defaults to None (for tokenzie call_type). 

        Returns:
            results: dict (contains keys i.e. tag, pos, dep)
        """

        if call_type == 'encode':
            if type(inputs) == str:
                return self.encode(inputs, max_seq=max_seq)
            else:
                print('input type error !')
        
        elif call_type == 'encode_plus':
            return self.encode_plus(inputs, max_seq=max_seq)

        elif call_type == 'tokenizer':
            return self.tokenizer(inputs)

        else:
            print(call_type, 'is not defined !')

        return None

    def encode(self, text, max_seq=128):
        """`encode` method allow to encode text into ids with max_seq lenght

        Args:

            text (string): input text

            max_seq (int, optional): Defaults to 128.

        Returns:

            results: dict
        """
        doc = nlp(text)
        results = {}

        if 'pos' in self.parsers:
            p_token = [token.pos_ for token in doc]
            p_token = self.convert_tokens_to_ids(p_token, 'pos')
            p_token = self.__add_padding(p_token, max_seq)
            results['pos'] = p_token
        if 'tag' in self.parsers:
            t_token = [token.tag_ for token in doc]
            t_token = self.convert_tokens_to_ids(t_token, 'tag')
            t_token = self.__add_padding(t_token, max_seq)
            results['tag'] = t_token
                
        if 'dep' in self.parsers:
            d_token = [token.dep_ for token in doc]
            d_token = self.convert_tokens_to_ids(d_token, 'dep')
            d_token = self.__add_padding(d_token, max_seq)
            results['dep'] = d_token

        return results

    def encode_plus(self, input_texts, max_seq=128):

        """`encode_plus` method allow to encode list of text into list of ids with max_seq lenght

        Args:

            input_texts (List): List of text

            max_seq (int, optional): Defaults to 128.

        Returns:

            results: dict
        """

        docs = nlp.pipe(input_texts, n_threads = 4)
        pos_tokens = []
        tag_tokens = []
        dep_tokens = []

        for doc in tqdm(docs):
            if 'pos' in self.parsers:
                p_token = [token.pos_ for token in doc]
                p_token = self.convert_tokens_to_ids(p_token, 'pos')
                p_token = self.__add_padding(p_token, max_seq)
                pos_tokens.append(p_token)
                
            if 'tag' in self.parsers:
                t_token = [token.tag_ for token in doc]
                t_token = self.convert_tokens_to_ids(t_token, 'tag')
                t_token = self.__add_padding(t_token, max_seq)
                tag_tokens.append(t_token)
                
            if 'dep' in self.parsers:
                d_token = [token.dep_ for token in doc]
                d_token = self.convert_tokens_to_ids(d_token, 'dep')
                d_token = self.__add_padding(d_token, max_seq)
                dep_tokens.append(d_token)

        results = {}

        if 'pos' in self.parsers:
            results['pos'] = pos_tokens
        if 'tag' in self.parsers:
            results['tag'] = tag_tokens
        if 'dep' in self.parsers:
            results['dep'] = dep_tokens

        return results

    

    def tokenize(self, input_texts):
        """`tokenizer` method allow to tokenize text

        Args:

            input_texts (List): Takes list of text(string)

        Returns:

            results: dict
        """

        docs = nlp.pipe(input_texts, n_threads = 4)
        pos_tokens = []
        tag_tokens = []
        dep_tokens = []

        for doc in tqdm(docs):
            if 'pos' in self.parsers:
                pos_tokens.append([token.pos_ for token in doc])
            if 'tag' in self.parsers:
                tag_tokens.append([token.tag_ for token in doc])
            if 'dep' in self.parsers:
                dep_tokens.append([token.dep_ for token in doc])

        results = {}

        if 'pos' in self.parsers:
            results['pos'] = pos_tokens
        if 'tag' in self.parsers:
            results['tag'] = tag_tokens
        if 'dep' in self.parsers:
            results['dep'] = dep_tokens

        return results

    def convert_tokens_to_ids(self, tokens, parser_type='pos'):
        if parser_type == 'pos':
            return convert_by_vocab(self.pos_vocab, tokens)
        if parser_type == 'tag':
            return convert_by_vocab(self.tag_vocab, tokens)
        if parser_type == 'dep':
            return convert_by_vocab(self.dep_vocab, tokens)
        else:
            print('Error: '+parser_type+' Parse is not defined !')
            return None
        

    def convert_ids_to_tokens(self, ids, parser_type='pos'):
        if parser_type == 'pos':
            return convert_by_vocab(self.inv_pos_vocab, ids)
        if parser_type == 'tag':
            return convert_by_vocab(self.inv_tag_vocab, ids)
        if parser_type == 'dep':
            return convert_by_vocab(self.inv_dep_vocab, ids)
        else:
            print('Error: '+parser_type+' Parse is not defined !')
            return None



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
    for i in tqdm(range(len(texts))):
        text = texts[i]
        tok1,tok2, tok3 = get_tokens(text)
        tok1 = add_padding(tok1, max_seq_length)
        tok2 = add_padding(tok2, max_seq_length)
        tok2 = add_padding(tok3, max_seq_length)
        tokens1.append(tok1)
        tokens2.append(tok2)
        tokens3.append(tok3)
        
    return np.array(tokens1), np.array(tokens2), np.array(tokens3)