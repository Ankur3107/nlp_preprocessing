```python
from nlp_preprocessing.dataset import Dataset
```

`Dataset` allow to split in test-train and encode (label or one-hot). It allow both multi-label and multi-class split


<h2 id="Dataset" class="doc_header"><code>class</code> <code>Dataset</code><a href="https://github.com/Ankur3107/nlp_preprocessing/blob/master/nlp_preprocessing/dataset.py#L6" class="source_link" style="float:right">[source]</a></h2>

> <code>Dataset</code>(**`data_config`**)

`Dataset` allow split and encoding using external config file

Args:

    data_config (dict): config dict
    example:
        data_config = {
                    'data_class':'multi-class',
                    'x_columns':[],
                    'y_columns':[],
                    'one_hot_encoded_columns':[],
                    'label_encoded_columns':[],
                    'data':None,
                    'split_ratio':0.2,
                    'random_state':3107
                }
        where data_class: ['multi-class','multi-label'] and data: it should be dataframe


Example


```python
import pandas as pd
text = ['I am Test 1','I am Test 2']
label = ['A','B']
aspect = ['C','D']
data = pd.DataFrame({'text':text*5,'label':label*5,'aspect':aspect*5})
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>text</th>
      <th>label</th>
      <th>aspect</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>I am Test 1</td>
      <td>A</td>
      <td>C</td>
    </tr>
    <tr>
      <th>1</th>
      <td>I am Test 2</td>
      <td>B</td>
      <td>D</td>
    </tr>
    <tr>
      <th>2</th>
      <td>I am Test 1</td>
      <td>A</td>
      <td>C</td>
    </tr>
    <tr>
      <th>3</th>
      <td>I am Test 2</td>
      <td>B</td>
      <td>D</td>
    </tr>
    <tr>
      <th>4</th>
      <td>I am Test 1</td>
      <td>A</td>
      <td>C</td>
    </tr>
    <tr>
      <th>5</th>
      <td>I am Test 2</td>
      <td>B</td>
      <td>D</td>
    </tr>
    <tr>
      <th>6</th>
      <td>I am Test 1</td>
      <td>A</td>
      <td>C</td>
    </tr>
    <tr>
      <th>7</th>
      <td>I am Test 2</td>
      <td>B</td>
      <td>D</td>
    </tr>
    <tr>
      <th>8</th>
      <td>I am Test 1</td>
      <td>A</td>
      <td>C</td>
    </tr>
    <tr>
      <th>9</th>
      <td>I am Test 2</td>
      <td>B</td>
      <td>D</td>
    </tr>
  </tbody>
</table>
</div>




```python
data_config = {
                'data_class':'multi-class',
                'x_columns':['text','aspect'],
                'y_columns':['label'],
                'one_hot_encoded_columns':[],
                'label_encoded_columns':['label','aspect'],
                'data':data,
                'split_ratio':0.2
              }
dataset = Dataset(data_config)
```


```python
dataset.data_config
```




    {'data_class': 'multi-class',
     'x_columns': ['text', 'aspect'],
     'y_columns': ['label'],
     'one_hot_encoded_columns': [],
     'label_encoded_columns': ['label', 'aspect'],
     'data':           text label aspect
     0  I am Test 1     A      C
     1  I am Test 2     B      D
     2  I am Test 1     A      C
     3  I am Test 2     B      D
     4  I am Test 1     A      C
     5  I am Test 2     B      D
     6  I am Test 1     A      C
     7  I am Test 2     B      D
     8  I am Test 1     A      C
     9  I am Test 2     B      D,
     'split_ratio': 0.2,
     'random_state': 3107}




```python
train, test = dataset.get_train_test_data()
train['Y_train'],train['X_train']
```




    ({'label': array([0, 1, 1, 0, 0, 1, 0, 1])},
     {'text': array(['I am Test 1', 'I am Test 2', 'I am Test 2', 'I am Test 1',
             'I am Test 1', 'I am Test 2', 'I am Test 1', 'I am Test 2'],
            dtype=object), 'aspect': array([0, 1, 1, 0, 0, 1, 0, 1])})




```python
test['Y_test'],test['X_test']
```




    ({'label': array([0, 1])},
     {'text': array(['I am Test 1', 'I am Test 2'], dtype=object),
      'aspect': array([0, 1])})