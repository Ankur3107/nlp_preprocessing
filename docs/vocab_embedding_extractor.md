
```python
from nlp_preprocessing.vocab_embedding_extractor import VocabEmbeddingExtractor
```

`VocabEmbeddingExtractor` allow to extract vocab and corrosponding embeddings from word2vec, fasttext, glove etc. word embeddings



<h2 id="VocabEmbeddingExtractor" class="doc_header"><code>class</code> <code>VocabEmbeddingExtractor</code><a href="nlp_preprocessing/vocab_embedding_extractor.py#L24" class="source_link" style="float:right">[source]</a></h2>

> <code>VocabEmbeddingExtractor</code>(**`vector_file`**, **`input_file`**, **`column_name`**)

`VocabEmbeddingExtractor` takes files(input file, vector file) and extract vocab and corrosponding embeddings from word2vec, fasttext, glove etc. word embeddings

Args:

    vector_file (string): external vector file i.e. word2vec, glove, fasttext

    input_file (string): input file in csv

    column_name (string): text column name from input file




<h4 id="VocabEmbeddingExtractor.process" class="doc_header"><code>VocabEmbeddingExtractor.process</code><a href="nlp_preprocessing/vocab_embedding_extractor.py#L42" class="source_link" style="float:right">[source]</a></h4>

> <code>VocabEmbeddingExtractor.process</code>(**`output_dir`**, **`special_tokens`**=*`[]`*)

`process` method allow to process and save output to output_dir

Args:

    output_dir (string): output directory

    special_tokens (list of string, optional): List all special tokens i.e [PAD], [SEP] . Defaults to [].


Example


```python
vector_file='../input/fasttext-crawl-300d-2m-with-subword/crawl-300d-2m-subword/crawl-300d-2M-subword.vec'
input_file='../input/complete-tweet-sentiment-extraction-data/tweet_dataset.csv'
column_name='text'

extractor = VocabEmbeddingExtractor(vector_file, input_file, column_name)
output_dir = '.'
special_tokens = ['[UNK]','[SEP]']
extractor.process(output_dir, special_tokens)
```
