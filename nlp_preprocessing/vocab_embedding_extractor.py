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


class WordEmbedding():
    def __init__(self, vector_file, embedding_size=300):
        self.vector_file = vector_file
        self.embedding_size = embedding_size

    def get_embeddings(self, vocab):

        vectors_dict = load_vectors(self.vector_file, 'embedding', vocab)
        return self.__get_final_embeddings(vectors_dict, vocab)

    def __get_final_embeddings(self, vectors_dict, vocab):
        results = {}

        for k, v in vocab.items():
            if k in vectors_dict:
                results[k] = vectors_dict[k]
            else:
                results[k] = list(np.random.uniform(-1,1,self.embedding_size))
                
        return np.array(list(results.values()))
        
        
class VocabEmbeddingExtractor():
    """`VocabEmbeddingExtractor` takes files(input file, vector file) and extract vocab and corrosponding embeddings from fasttext word embeddings

        Args:

            vector_file (string): external vector file i.e. currently only compatible for fasttext vestor file

            input_file (string): input file in csv

            column_name (string): text column name from input file

        """
    def __init__(self, vector_file, texts=None, input_file=None, column_name=None, embedding_size=300):
        
        if texts:
            self.texts = texts
        elif input_file and column_name:
            self.input_file = input_file
            self.column_name = column_name
            df = pd.read_csv(self.input_file)
            self.texts = df[self.column_name].values.tolist()

        else:
            print('Please enter either texts or input_file, column_name')

        self.vector_file = vector_file
        self.embedding_size = embedding_size
        
    def process(self, output_dir, special_tokens=[]):
        """`process` method allow to process and save output to output_dir

        Args:

            output_dir (string): output directory

            special_tokens (list of string, optional): List all special tokens i.e [PAD], [SEP] . Defaults to [].
        """

        vectors_dict = load_vectors(self.vector_file)

        full_vocab_file = output_dir+'/full_vocab.txt'
        full_vocab = list(vectors_dict.keys())
        full_vocab.extend(special_tokens)
        
        self.__write(full_vocab, full_vocab_file)

        full_vocab_tokenizer = FullTokenizer(
            vocab_file=full_vocab_file, do_lower_case=True)
        
        unique_subword = self.__get_unique(full_vocab_tokenizer, self.texts)

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
            embedding_list.append(list(np.random.uniform(-1,1,self.embedding_size)))

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