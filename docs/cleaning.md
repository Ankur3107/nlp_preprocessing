## <center>Text Cleaning </center>

The `nlp_preprocessing.clean` module allow efficient way of text cleaning.


```python
from nlp_preprocessing.clean import *
```

`Clean` class initiator takes ordered list of cleaning functions(list given below) and using `__call__` function we can apply each function on list of string.

    CLEAN_FUNS = {
        'to_lower' : to_lower(),
        'to_normalize' : to_normalize(),
        'remove_href' : remove_href(),
        'remove_control_char' : remove_control_char(),
        'remove_duplicate' : remove_duplicate(),
        'remove_underscore' : remove_underscore(),
        'seperate_spam_chars' : seperate_spam_chars(),
        'seperate_brakets_quotes' : seperate_brakets_quotes(),
        'break_short_words' : break_short_words(),
        'break_long_words' : break_long_words(),
        'remove_ending_underscore' : remove_ending_underscore(),
        'remove_starting_underscore' : remove_starting_underscore(),
        'seperate_end_word_punctuations' : seperate_end_word_punctuations(),
        'seperate_start_word_punctuations' : seperate_start_word_punctuations(),
        'clean_contractions' : clean_contractions(),
        'remove_s' : remove_s(),
        'isolate_numbers' : isolate_numbers(),
        'regex_split_word' : regex_split_word(),
        'leet_clean' : leet_clean(),
        'clean_open_holded_words' : clean_open_holded_words(),
        'clean_multiple_form' : clean_multiple_form()
    }



<h2 id="Clean" class="doc_header"><code>class</code> <code>Clean</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L686" class="source_link" style="float:right">[source]</a></h2>

> <code>Clean</code>(**`clean_fn_ordered_list`**=*`['to_lower', 'to_normalize', 'remove_href', 'remove_control_char', 'remove_duplicate', 'remove_underscore', 'seperate_spam_chars', 'seperate_brakets_quotes', 'break_short_words', 'break_long_words', 'remove_ending_underscore', 'remove_starting_underscore', 'seperate_end_word_punctuations', 'seperate_start_word_punctuations', 'clean_contractions', 'remove_s', 'isolate_numbers', 'regex_split_word', 'leet_clean', 'clean_open_holded_words', 'clean_multiple_form']`*)




Examples:


```python
texts = ['Hi, how are you', "I am's good"]
cleaned_text = Clean()(texts)
print('Output :', cleaned_text)
```

    ########## Step - Lowering everything:
    ########## Step - Normalize chars and dots:
    ########## Step - Remove hrefs:
    ########## Step - Control Chars:
    ########## Step - Duplicated Chars:
    Total Words : 7
    ########## Step - Remove underscore:
    Total Words : 7
    ['hi, how are you']
    ########## Step - Spam chars repetition:
    Total Words : 7
    {}
    ########## Step - Brackets and quotes:
    ########## Step - Break long words:
    ########## Step - Break long words:
    ########## Step - Remove ending underscore:
    Total Words : 7
    ########## Step - Remove starting underscore:
    Total Words : 7
    ########## Step - End word punctuations:
    hi, --- hi ,
    ########## Step - Start word punctuations:
    ########## Step - Contractions:
    Total Words : 8
    ########## Step - Remove "s:
    Total Words : 8
    am's --- am
    ########## Step - Isolate numbers:
    Total Words : 8
    Total Words : 8
    , ---  , 
    ########## Step - L33T (with vocab check):
    Total Words : 8
    ########## Step - Open Holded words:
    ########## Step - Multiple form:
    Total Words : 8
    Output : ['hi , how are you', 'i am good']



```python
texts = ['Hi, how are you', "I am's good"]
cleaned_text = Clean(['to_lower','remove_s','seperate_end_word_punctuations'])(texts)
print('Output :', cleaned_text)
```

    ########## Step - Lowering everything:
    ########## Step - Remove "s:
    Total Words : 7
    am's --- am
    ########## Step - End word punctuations:
    hi, --- hi ,
    Output : ['hi , how are you', 'i am good']


All cleaning functions takes list of string as input and map function on it



<h4 id="to_lower" class="doc_header"><code>to_lower</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L55" class="source_link" style="float:right">[source]</a></h4>

> <code>to_lower</code>(**`data`**)





<h4 id="to_normalize" class="doc_header"><code>to_normalize</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L60" class="source_link" style="float:right">[source]</a></h4>

> <code>to_normalize</code>(**`data`**)





<h4 id="remove_href" class="doc_header"><code>remove_href</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L105" class="source_link" style="float:right">[source]</a></h4>

> <code>remove_href</code>(**`data`**)





<h4 id="remove_control_char" class="doc_header"><code>remove_control_char</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L97" class="source_link" style="float:right">[source]</a></h4>

> <code>remove_control_char</code>(**`data`**)





<h4 id="remove_duplicate" class="doc_header"><code>remove_duplicate</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L110" class="source_link" style="float:right">[source]</a></h4>

> <code>remove_duplicate</code>(**`data`**)





<h4 id="remove_underscore" class="doc_header"><code>remove_underscore</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L136" class="source_link" style="float:right">[source]</a></h4>

> <code>remove_underscore</code>(**`data`**)





<h4 id="seperate_spam_chars" class="doc_header"><code>seperate_spam_chars</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L150" class="source_link" style="float:right">[source]</a></h4>

> <code>seperate_spam_chars</code>(**`data`**)





<h4 id="seperate_brakets_quotes" class="doc_header"><code>seperate_brakets_quotes</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L163" class="source_link" style="float:right">[source]</a></h4>

> <code>seperate_brakets_quotes</code>(**`data`**)





<h4 id="break_short_words" class="doc_header"><code>break_short_words</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L170" class="source_link" style="float:right">[source]</a></h4>

> <code>break_short_words</code>(**`data`**)





<h4 id="break_long_words" class="doc_header"><code>break_long_words</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L186" class="source_link" style="float:right">[source]</a></h4>

> <code>break_long_words</code>(**`data`**)





<h4 id="remove_ending_underscore" class="doc_header"><code>remove_ending_underscore</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L206" class="source_link" style="float:right">[source]</a></h4>

> <code>remove_ending_underscore</code>(**`data`**)





<h4 id="remove_starting_underscore" class="doc_header"><code>remove_starting_underscore</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L224" class="source_link" style="float:right">[source]</a></h4>

> <code>remove_starting_underscore</code>(**`data`**)





<h4 id="seperate_end_word_punctuations" class="doc_header"><code>seperate_end_word_punctuations</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L242" class="source_link" style="float:right">[source]</a></h4>

> <code>seperate_end_word_punctuations</code>(**`data`**)





<h4 id="seperate_start_word_punctuations" class="doc_header"><code>seperate_start_word_punctuations</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L260" class="source_link" style="float:right">[source]</a></h4>

> <code>seperate_start_word_punctuations</code>(**`data`**)





<h4 id="clean_contractions" class="doc_header"><code>clean_contractions</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L278" class="source_link" style="float:right">[source]</a></h4>

> <code>clean_contractions</code>(**`data`**)





<h4 id="remove_s" class="doc_header"><code>remove_s</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L501" class="source_link" style="float:right">[source]</a></h4>

> <code>remove_s</code>(**`data`**)





<h4 id="isolate_numbers" class="doc_header"><code>isolate_numbers</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L511" class="source_link" style="float:right">[source]</a></h4>

> <code>isolate_numbers</code>(**`data`**)





<h4 id="regex_split_word" class="doc_header"><code>regex_split_word</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L532" class="source_link" style="float:right">[source]</a></h4>

> <code>regex_split_word</code>(**`data`**)





<h4 id="leet_clean" class="doc_header"><code>leet_clean</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/clean.py#L552" class="source_link" style="float:right">[source]</a></h4>

> <code>leet_clean</code>(**`data`**)





<h4 id="clean_open_holded_words" class="doc_header"><code>clean_open_holded_words</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L579" class="source_link" style="float:right">[source]</a></h4>

> <code>clean_open_holded_words</code>(**`data`**)





<h4 id="clean_multiple_form" class="doc_header"><code>clean_multiple_form</code><a href="nhttps://github.com/Ankur3107/nlp_preprocessing/blob/master/lp_preprocessing/clean.py#L592" class="source_link" style="float:right">[source]</a></h4>

> <code>clean_multiple_form</code>(**`data`**)





```python

```


