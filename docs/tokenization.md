```python
from nlp_preprocessing.seq_token_generator import *
```

`SpacyTokenizer` allow to tokenize your text. `__call__` method can 


<h2 id="SpacyTokenizer" class="doc_header"><code>class</code> <code>SpacyTokenizer</code><a href="nlp_preprocessing/seq_token_generator.py#L40" class="source_link" style="float:right">[source]</a></h2>

> <code>SpacyTokenizer</code>(**`vocab_file`**=*`None`*, **`spacy_tokenizer`**=*`<spacy.tokenizer.Tokenizer object at 0x167c88950>`*, **`special_token`**=*`['[PAD]']`*, **`pad_token_index`**=*`0`*)



<h4 id="SpacyTokenizer.__call__" class="doc_header"><code>SpacyTokenizer.__call__</code><a href="nlp_preprocessing/seq_token_generator.py#L150" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyTokenizer.__call__</code>(**`inputs`**, **`call_type`**=*`'tokenize'`*, **`max_seq`**=*`None`*)

`__call__` method allow to call encode, encode_plus and tokenize from single interface.

Args:

    inputs (List or string): Input can be string or list of text

    call_type (str, optional): can be encode, encode_plus, tokenize. Defaults to 'tokenize'.

    max_seq ([type], optional): it applies for encode and encode_plus call_type Defaults to None (for tokenzie call_type). 


Returns:

    tokens or ids: List or List of List


<h4 id="SpacyTokenizer.encode" class="doc_header"><code>SpacyTokenizer.encode</code><a href="nlp_preprocessing/seq_token_generator.py#L95" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyTokenizer.encode</code>(**`text`**, **`max_seq`**=*`128`*)

`encode` method allow to encode text into ids with max_seq lenght

Args:

    text (string): input text

    max_seq (int, optional): Defaults to 128.

Returns:

    tokens: List of token




<h4 id="SpacyTokenizer.encode_plus" class="doc_header"><code>SpacyTokenizer.encode_plus</code><a href="nlp_preprocessing/seq_token_generator.py#L120" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyTokenizer.encode_plus</code>(**`input_texts`**, **`max_seq`**=*`128`*)

`encode_plus` method allow to encode list of text into list of ids with max_seq lenght

Args:

    input_texts (List): List of text

    max_seq (int, optional): Defaults to 128.

Returns:

    tokens: List of List of token



<h4 id="SpacyTokenizer.tokenize" class="doc_header"><code>SpacyTokenizer.tokenize</code><a href="nlp_preprocessing/seq_token_generator.py#L60" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyTokenizer.tokenize</code>(**`input_texts`**)

`tokenizer` method allow to tokenize text

Args:

    input_texts (List): Takes list of text(string)

Returns:

    tokens: List[List]


Examples


```python
texts = ['Hi, how are you', "I am good"]
tokens = SpacyTokenizer()(texts, call_type='tokenize')
print('Output :',tokens)
```

    2it [00:00,  4.64it/s]

    Output : [['Hi', ',', 'how', 'are', 'you'], ['I', 'am', 'good']]


    



```python
texts = ['Hi, how are you', "I am good"]
spacy_tokenizer = SpacyTokenizer()
tokens = spacy_tokenizer.tokenize(texts)
ids =  [spacy_tokenizer.convert_tokens_to_ids(token) for token in tokens]
print('Tokens : ',tokens)
print('Token_ids : ', ids)
print('Vocab : ', spacy_tokenizer.vocab)
```

    2it [00:00, 79.79it/s]

    Tokens :  [['Hi', ',', 'how', 'are', 'you'], ['I', 'am', 'good']]
    Token_ids :  [[1, 2, 3, 4, 5], [6, 7, 8]]
    Vocab :  {'[PAD]': 0, 'Hi': 1, ',': 2, 'how': 3, 'are': 4, 'you': 5, 'I': 6, 'am': 7, 'good': 8}


    



```python
texts = ['Hi, how are you', "I am good"]
spacy_tokenizer = SpacyTokenizer()
ids = spacy_tokenizer.encode_plus(texts, max_seq=10)
print('Token_ids : ', ids)
print('Vocab : ', spacy_tokenizer.vocab)
```

    2it [00:00, 80.31it/s]

    Token_ids :  [[1, 2, 3, 4, 5, 0, 0, 0, 0, 0], [6, 7, 8, 0, 0, 0, 0, 0, 0, 0]]
    Vocab :  {'[PAD]': 0, 'Hi': 1, ',': 2, 'how': 3, 'are': 4, 'you': 5, 'I': 6, 'am': 7, 'good': 8}


    



```python
spacy_tokenizer = SpacyTokenizer()
ids = spacy_tokenizer.encode('Hi, how are you', max_seq=10)
print('Token Ids :', ids)
print('Vocab : ', spacy_tokenizer.vocab)
```

    Token Ids : [1, 2, 3, 4, 5, 0, 0, 0, 0, 0]
    Vocab :  {'[PAD]': 0, 'Hi': 1, ',': 2, 'how': 3, 'are': 4, 'you': 5}



```python
from nlp_preprocessing.seq_parser_token_generator import *
```

`SpacyParseTokenizer` allow to tokenize text and get different parse tokens i.e. dependency parse, tag parse, pos parse from Spacy model 



<h2 id="SpacyParseTokenizer" class="doc_header"><code>class</code> <code>SpacyParseTokenizer</code><a href="nlp_preprocessing/seq_parser_token_generator.py#L142" class="source_link" style="float:right">[source]</a></h2>

> <code>SpacyParseTokenizer</code>(**`parsers`**=*`['pos', 'tag', 'dep']`*)



<h4 id="SpacyParseTokenizer.__call__" class="doc_header"><code>SpacyParseTokenizer.__call__</code><a href="nlp_preprocessing/seq_parser_token_generator.py#L163" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyParseTokenizer.__call__</code>(**`inputs`**, **`call_type`**=*`'tokenize'`*, **`max_seq`**=*`None`*)

`__call__` method allow a single interface to call encode, encode_plus and tokenize methods

Args:

    inputs (List or string): It can be string (for encode call type) or List for encode_plus and tokenize

    call_type (str, optional): can be encode, encode_plus, tokenize. Defaults to 'tokenize'.

    max_seq ([type], optional): it applies for encode and encode_plus call_type Defaults to None (for tokenzie call_type). 

Returns:
    results: dict (contains keys i.e. tag, pos, dep)


<h4 id="SpacyParseTokenizer.tokenize" class="doc_header"><code>SpacyParseTokenizer.tokenize</code><a href="nlp_preprocessing/seq_parser_token_generator.py#L282" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyParseTokenizer.tokenize</code>(**`input_texts`**)

`tokenizer` method allow to tokenize text

Args:

    input_texts (List): Takes list of text(string)

Returns:

    results: dict


<h4 id="SpacyParseTokenizer.encode" class="doc_header"><code>SpacyParseTokenizer.encode</code><a href="nlp_preprocessing/seq_parser_token_generator.py#L195" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyParseTokenizer.encode</code>(**`text`**, **`max_seq`**=*`128`*)

`encode` method allow to encode text into ids with max_seq lenght

Args:

    text (string): input text

    max_seq (int, optional): Defaults to 128.

Returns:

    results: dict


<h4 id="SpacyParseTokenizer.encode_plus" class="doc_header"><code>SpacyParseTokenizer.encode_plus</code><a href="nlp_preprocessing/seq_parser_token_generator.py#L230" class="source_link" style="float:right">[source]</a></h4>

> <code>SpacyParseTokenizer.encode_plus</code>(**`input_texts`**, **`max_seq`**=*`128`*)

`encode_plus` method allow to encode list of text into list of ids with max_seq lenght

Args:

    input_texts (List): List of text

    max_seq (int, optional): Defaults to 128.

Returns:

    results: dict


Examples


```python
texts = ['Hi, how are you', "I am good"]
tokens = SpacyParseTokenizer()(texts, call_type='tokenize')
print('Output :',tokens)
```

    2it [00:00, 51.19it/s]

    Output : {'pos': [['INTJ', 'PUNCT', 'ADV', 'AUX', 'PRON'], ['PRON', 'AUX', 'ADJ']], 'tag': [['UH', ',', 'WRB', 'VBP', 'PRP'], ['PRP', 'VBP', 'JJ']], 'dep': [['intj', 'punct', 'advmod', 'ROOT', 'nsubj'], ['nsubj', 'ROOT', 'acomp']]}


    



```python
texts = ['Hi, how are you', "I am good"]
tokens = SpacyTokenizer()(texts, call_type='tokenize')
parse_tokens = SpacyParseTokenizer()(texts, call_type='tokenize')
print('Output : ',tokens)
print('Parse Dict : ', parse_tokens)
```

    2it [00:00, 70.61it/s]
    2it [00:00, 54.82it/s]

    Output :  [['Hi', ',', 'how', 'are', 'you'], ['I', 'am', 'good']]
    Parse Dict :  {'pos': [['INTJ', 'PUNCT', 'ADV', 'AUX', 'PRON'], ['PRON', 'AUX', 'ADJ']], 'tag': [['UH', ',', 'WRB', 'VBP', 'PRP'], ['PRP', 'VBP', 'JJ']], 'dep': [['intj', 'punct', 'advmod', 'ROOT', 'nsubj'], ['nsubj', 'ROOT', 'acomp']]}
