# <center>text-preprocessing<center/>

***text-preprocessing*** provides text preprocessing functions i.e. text cleaning, dataset preprocessing, tokenization etc

#### Installation

    pip install text-preprocessing

## Tutorial

### 1. Text Cleaning

    from nlp_preprocessing import clean

    texts = ["Hi I am's nakdur"]
    cleaned_texts = clean.clean_v1(texts)

There are multiple cleaning functions:

    data_list = to_lower(data_list)
    data_list = to_normalize(data_list)
    data_list = remove_href(data_list)
    data_list = remove_control_char(data_list)
    data_list = remove_duplicate(data_list)
    data_list = remove_underscore(data_list)
    data_list = seperate_spam_chars(data_list)
    data_list = seperate_brakets_quotes(data_list)
    data_list = break_short_words(data_list)
    data_list = break_long_words(data_list)
    data_list = remove_ending_underscore(data_list)
    data_list = remove_starting_underscore(data_list)
    data_list = seperate_end_word_punctuations(data_list)
    data_list = seperate_start_word_punctuations(data_list)
    data_list = clean_contractions(data_list)
    data_list = remove_s(data_list)
    data_list = isolate_numbers(data_list)
    data_list = regex_split_word(data_list)
    data_list = leet_clean(data_list)
    data_list = clean_open_holded_words(data_list)
    data_list = clean_multiple_form(data_list)


### 2. Dataset Prepration

    from nlp_preprocessing import dataset as ds
    import pandas as pd

    text = ['I am Test 1','I am Test 2']
    label = ['A','B']
    aspect = ['C','D']
    data = pd.DataFrame({'text':text*5,'label':label*5,'aspect':aspect*5})
    data

    data_config = {
                'data_class':'multi-label',
                'x_columns':['text'],
                'y_columns':['label','aspect'],
                'one_hot_encoded_columns':[],
                'label_encoded_columns':['label','aspect'],
                'data':data,
                'split_ratio':0.1
              }

    dataset = ds.Dataset(data_config)
    train, test = dataset.get_train_test_data()

    print(train['Y_train'],train['X_train'])
    print(test['Y_test'],test['X_test'])
    print(dataset.data_config)


### 3.  Seq token generator

    texts = ['I am Test 2', 'I am Test 1', 'I am Test 1', 'I am Test 1','I am Test 1', 'I am Test 2', 'I am Test 1', 'I am Test 2','I am Test 2']

    tokens = seq_gen.get_word_sequences(texts)
    print(tokens)

### 4. Token embedding creator

    from nlp_preprocessing import token_embedding_creator

    vector_file='../input/fasttext-crawl-300d-2m-with-subword/crawl-300d-2m-subword/crawl-300d-2M-subword.vec'
    input_file='../input/complete-tweet-sentiment-extraction-data/tweet_dataset.csv'
    column_name='text'

    processor = token_embedding_creator.Processor(vector_file, input_file, column_name)
    output_dir = '.'
    special_tokens = ['[UNK]','[SEP]']
    
    processor.process(output_dir, special_tokens)

    #Loading vectors from  ../input/fasttext-crawl-300d-2m-with-subword/crawl-300d-2m-subword/crawl-300d-2M-subword.vec  type:  index
    #Writing vocab at  ./full_vocab.txt
    #1%|          | 218/40000 [00:00<00:18, 2176.72it/s]
    #Generating unique tokens ...
    #100%|██████████| 40000/40000 [00:18<00:00, 2180.53it/s]
    #Writing vocab at  ./vocab.txt
    #Loading vectors from  ../input/fasttext-crawl-300d-2m-with-subword/crawl-300d-2m-subword/crawl-300d-2M-subword.vec  type:  embedding
    #Writing vocab at  ./vocab.txt
    #Making Final Embedding ...
    #Writing embedding at  ./embeddings.npy
    #Processing Done !
    #Vocab stored at : ./vocab.txt  of size:  25475
    #Embedding stored at : ./embeddings.npy of shape:  (25475, 300)