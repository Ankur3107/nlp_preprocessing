# text-preprocessing

### 1. Text Cleaning

    from nlp_preprocessing import clean

    texts = ["Hi I am's nakdur"]
    cleaned_texts = clean.clean_v1(texts)


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

