from tensorflow.keras.preprocessing.sequence import pad_sequences
import spacy
import deepdish as dd
from tqdm import tqdm
import os


# GLobal Variable
nlp = spacy.load('en_core_web_sm', disable=['parser','ner','tagger'])
nlp.vocab.add_flag(lambda s: s.lower() in spacy.lang.en.stop_words.STOP_WORDS, spacy.attrs.IS_STOP)

def get_word_sequences(text_list, token_file_path=None, word_dict={}, lemma_dict={}, word_index=1, max_length = 250):
    
    if(token_file_path is not None) and os.path.exists(token_file_path):
        token_data = dd.io.load(token_file_path)
        word_dict = token_data['word_dict']
        lemma_dict = token_data['lemma_dict']
        word_index = token_data['word_index']
        
    previous_word_index = word_index
    docs = nlp.pipe(text_list, n_threads = 4)
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