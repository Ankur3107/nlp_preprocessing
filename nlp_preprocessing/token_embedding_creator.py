import io
import pandas as pd
from .tokenization import FullTokenizer, load_vocab
import tqdm
import numpy as np

def load_vectors(fname, type='index',vocab=None):
    print('Loading vectors from ', fname,' type: ',type)
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    i=1
    for line in fin:
        tokens = line.rstrip().split(' ')
        if type=='index':
            data[tokens[0]] = i
            i+=1
        else:
            if tokens[0] in vocab:
                data[tokens[0]] = list(map(float, tokens[1:]))
        
    return data

class Processor():
    def __init__(self,vector_file, input_file, column_name):
        self.vector_file = vector_file
        self.input_file = input_file
        self.column_name = column_name


    def process(self, output_dir, special_tokens=[]):

        vectors_dict = load_vectors(self.vector_file)
        df = pd.read_csv(self.input_file)

        full_vocab_file = output_dir+'/full_vocab.txt'
        full_vocab = list(vectors_dict.keys())
        full_vocab.extend(special_tokens)
        
        self.__write(full_vocab, full_vocab_file)

        full_vocab_tokenizer = FullTokenizer(
            vocab_file=full_vocab_file, do_lower_case=True)
        
        unique_subword = self.__get_unique(full_vocab_tokenizer, df[self.column_name].values)

        vocab_file = output_dir+'/vocab.txt'
        self.__write(unique_subword, vocab_file)

        new_vocab = load_vocab(vocab_file)
        new_vectors_dict = load_vectors(self.vector_file, 'embedding', new_vocab)

        final_vocab = list(new_vectors_dict.keys())
        final_vocab.extend(special_tokens)

        self.__write(final_vocab, vocab_file)
        embedding_matrix = self.__get_final_embedding(list(new_vectors_dict.values()), special_tokens)

        embedding_file = output_dir+'/embeddings.npy'
        self.__write_final_embedding(embedding_matrix, embedding_file)

        print('Processing Done !')
        print('Vocab stored at :',vocab_file ,' of size: ',len(final_vocab))
        print('Embedding stored at :', embedding_file, 'of shape: ', embedding_matrix.shape)

    def __get_final_embedding(self, embedding_list, special_tokens):
        print('Making Final Embedding ...')
        for t in special_tokens:
            embedding_list.append(list(np.random.uniform(-1,1,300)))

        embedding_matrix = np.array(embedding_list)
        return embedding_matrix

    def __write_final_embedding(self, embedding_matrix, embedding_file):
        print('Writing embedding at ', embedding_file)
        np.save(embedding_file, embedding_matrix)


    def __get_unique(self, tokenizer, text_list):
        print('Generating unique tokens ...')
        unique_subword = set()
        unknown_count = 0
        for i in tqdm.tqdm(range(len(text_list))):
            subword_list = tokenizer.tokenize(str(text_list[i]))
            
            for subword in subword_list:
                if subword=='[UNK]':
                    unknown_count+=1
                unique_subword.add(subword)
        
        print('No of unique subwords :', len(list(unique_subword)))
        print('No of Unknowns:', unknown_count)
        return list(unique_subword)

    def __write(self, text_list, file_name):
        print('Writing vocab at ', file_name)
        with open(file_name, 'w') as file:
            for key in text_list:
                file.write(key)
                file.write('\n')