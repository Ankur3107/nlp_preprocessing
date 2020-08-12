from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy
import deepdish as dd
from tqdm import tqdm
import os


try:
    nlp = spacy.load('en_core_web_sm')
    spacy_tokenizer = nlp.tokenizer
except OSError:
    print('Downloading language model for the spaCy POS tagger\n'
        "(don't worry, this will only happen once)", file=stderr)
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm', disable=['parser','ner','tagger'])
    spacy_tokenizer = nlp.tokenizer

def load_vocab(vocab_file):
  """Loads a vocabulary file into a dictionary."""
  vocab = collections.OrderedDict()
  index = 0
  with open(vocab_file, "r") as reader:
    while True:
      token = convert_to_unicode(reader.readline())
      if not token:
        break
      token = token.strip()
      vocab[token] = index
      index += 1
  return vocab

def convert_by_vocab(vocab, items):
  """Converts a sequence of [tokens|ids] using the vocab."""
  output = []
  for item in items:
    output.append(vocab[item])
  return output

class SpacyTokenizer():

    def __init__(self, vocab_file=None, spacy_tokenizer=spacy_tokenizer, special_token=['[PAD]'], pad_token_index=0):
        self.tokenizer = spacy_tokenizer
        self.vocab = load_vocab(vocab_file) if vocab_file else self.__get_initial_vocab(special_token)
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        self.current_index = len(self.vocab)
        self.pad_token_index = pad_token_index

    def __get_initial_vocab(self, special_tokens):
        vocab = {}
        index = 0
        for t in special_tokens:
            if t not in vocab:
                vocab[t] = index
                index+=1
        self.vocab = vocab
        self.current_index = index
        return self.vocab
        

    def tokenize(self, input_texts):
        docs = self.tokenizer.pipe(input_texts, n_threads = 4)
        
        output_tokens = []
        for doc in tqdm(docs):
            output_tokens.append([token.text for token in doc])
            for token in doc:
                if (token.text not in self.vocab):
                    self.vocab[token.text] = self.current_index
                    self.current_index += 1
        
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        return output_tokens

    def __add_padding(self, tokens, max_seq):

        if len(tokens)==max_seq:
            return tokens
        elif len(tokens) > max_seq:
            return tokens[0:max_seq]
        else:
            while(len(tokens)<max_seq):
                tokens.append(self.pad_token_index)
            return tokens

    def encode(self, text, max_seq=128):
        doc = self.tokenizer(text)

        tokens = [token.text for token in doc]
        for token in doc:
            if (token.text not in self.vocab):
                self.vocab[token.text] = self.current_index
                self.current_index += 1
        tokens = self.convert_tokens_to_ids(tokens)
        tokens = self.__add_padding(tokens, max_seq)

        return tokens

    def encode_plus(self, input_texts, max_seq=128):

        docs = self.tokenizer.pipe(input_texts, n_threads = 4)
        
        output_tokens = []
        for doc in tqdm(docs):
            token_seq = []
            for token in doc:
                if (token.text not in self.vocab):
                    self.vocab[token.text] = self.current_index
                    self.current_index += 1
                token_seq.append(self.vocab[token.text])
            token_seq = self.__add_padding(token_seq, max_seq)
            output_tokens.append(token_seq)
        
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
        return output_tokens

    def __call__(self, inputs, call_type='encode', max_seq=None):

        if call_type == 'encode':
            if type(inputs) == str:
                return self.encode(inputs, max_seq=max_seq)
            else:
                print('input type error !')
        
        elif call_type == 'encode_plus':
            return self.encode_plus(inputs, max_seq=max_seq)

        elif call_type == 'tokenize':
            return self.tokenize(inputs)

        else:
            print(call_type, 'is not defined !')

        return None
    
    def convert_tokens_to_ids(self, tokens):
        return convert_by_vocab(self.vocab, tokens)
    
    def convert_ids_to_tokens(self, ids):
        return convert_by_vocab(self.inv_vocab, ids)
    


def get_word_sequences(text_list, token_file_path=None, word_dict={}, lemma_dict={}, word_index=1, max_length = 250):
    
    if(token_file_path is not None) and os.path.exists(token_file_path):
        token_data = dd.io.load(token_file_path)
        word_dict = token_data['word_dict']
        lemma_dict = token_data['lemma_dict']
        word_index = token_data['word_index']
        
    previous_word_index = word_index
    docs = nlp.tokenizer.pipe(text_list, n_threads = 4)
    word_sequences = []

    for doc in tqdm(docs):
        word_seq = []
        for token in doc:
            if (token.text not in word_dict) and (token.pos_ is not "PUNCT"):
                word_dict[token.text] = word_index
                word_index += 1
                lemma_dict[token.text] = token.lemma_
            if token.pos_ is not "PUNCT":
                word_seq.append(word_dict[token.text])
        word_sequences.append(word_seq)
    del docs
    
    if previous_word_index!=word_index and token_file_path!=None:
        print('Changes Saved at ', token_file_path)
        data = {'word_dict': word_dict, 'lemma_dict':lemma_dict, 'word_index':word_index}
        dd.io.save(token_file_path, data)
    
    return pad_sequences(word_sequences, max_length)

def get_tokenids_start_end_position(tokenizer, text, extracted_text,extra_text=None, verbose=False):

    text = '[CLS] '+text+' [SEP]'
    if extra_text:
        text = text+' '+extra_text+' [SEP]'
    index = text.find(extracted_text)
    
    first = tokenizer.tokenize(text[0:index])
    middle = tokenizer.tokenize(text[index:index+len(extracted_text)])
    last = tokenizer.tokenize(text[index+len(extracted_text):len(text)])
    
    if verbose:
        print(text[0:index], text[index:index+len(extracted_text)], text[index+len(extracted_text):len(text)])
    
    tokens = first+middle+last
    token_ids = tokenizer.convert_tokens_to_ids(tokens)
    start = len(first)
    end = len(first)+len(middle)
    
    return token_ids, start, end