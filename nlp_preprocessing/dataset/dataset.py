from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np

class Dataset():

    def __init__(self, data_config):
        self.data_config = self.__get_default_data_config()
        self.__temp_storage = {}

        for key, value in data_config.items():
            self.data_config[key] = value


    def __get_default_data_config(self):
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
        return data_config

    def __label_encode(self, data, name):
        name = name + "_factor"

        if name in self.__temp_storage:
            label_encoder = self.__temp_storage[name]
            encoded = label_encoder.fit_transform(data)
        else:
            label_encoder = LabelEncoder()
            self.__temp_storage[name] = label_encoder
            encoded = label_encoder.fit_transform(data)
            self.data_config[name] = np.array(label_encoder.classes_, dtype=object)

        return encoded

    def __one_hot_encode(self, data, name):
        
        name = name + "_factor"
        data = data.tolist()
        data = [[d] for d in data]

        if name in self.__temp_storage:
            onehot_encoder = self.__temp_storage[name]
            encoded = onehot_encoder.transform(data)
        else:
            onehot_encoder = OneHotEncoder(handle_unknown='ignore')
            onehot_encoder.fit(data)
            self.__temp_storage[name] = onehot_encoder
            encoded = onehot_encoder.transform(data)
            self.data_config[name] = np.array(onehot_encoder.categories_[0], dtype=object)
        return encoded.toarray()

    def __get_processed_data(self, data, type):

        result = {}
        for column in self.data_config[type]:

            if column in self.data_config['one_hot_encoded_columns']:
                result[column] = np.array(self.__one_hot_encode(data[column].values, column))
            elif column in self.data_config['label_encoded_columns']:
                result[column] = np.array(self.__label_encode(data[column].values, column))
            else:
                result[column] = np.array(data[column].values)
        return result
    

    def get_train_test_data(self):

        train = {}
        test = {}

        if self.data_config['data_class'] == 'multi-class':
            train_lines, test_lines, train_labels, test_labels = train_test_split(self.data_config['data'][self.data_config['x_columns']],
                                                                self.data_config['data'][self.data_config['y_columns']], 
                                                                test_size=self.data_config['split_ratio'], 
                                                                random_state=self.data_config['random_state'],
                                                                stratify=self.data_config['data'][self.data_config['y_columns']])
            X_train = self.__get_processed_data(train_lines,'x_columns')
            Y_train = self.__get_processed_data(train_labels,'y_columns')
            X_test = self.__get_processed_data(test_lines,'x_columns')
            Y_test = self.__get_processed_data(test_labels,'y_columns')

            train['X_train'] = X_train
            train['Y_train'] = Y_train
            test['X_test'] = X_test
            test['Y_test'] = Y_test
            
        elif self.data_config['data_class'] == 'multi-label':
            train_lines, test_lines, train_labels, test_labels = train_test_split(self.data_config['data'][self.data_config['x_columns']],
                                                                self.data_config['data'][self.data_config['y_columns']], 
                                                                test_size=self.data_config['split_ratio'], 
                                                                random_state=self.data_config['random_state'])

            X_train = self.__get_processed_data(train_lines,'x_columns')
            Y_train = np.array(train_labels)
            X_test = self.__get_processed_data(test_lines,'x_columns')
            Y_test = np.array(test_labels)

            train['X_train'] = X_train
            train['Y_train'] = Y_train
            test['X_test'] = X_test
            test['Y_test'] = Y_test
            
        else:
            print('Developing')
        
        return train, test