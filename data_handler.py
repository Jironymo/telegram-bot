"""  
Provides access to the Data_handler class, which is basically a general-purpose wrapper around a db file
with the following core self-explanatory methods of interest: 
    1. fetch_param(self, dep_param, indep_param, value);
    2. append_entry(self, param_dict);
""" 

class Data_handler:
    from typing import Dict

    """
    Initializes object of Data_handler type.
    Expects path to a data file as an initialization input param.
    Data_handler obj allows storing data files in-memory, fetch data based on provided params, put data into a db file.   
    """
    # a mask over db to distinguish between categorical and non-categorical data
    categorical_mask = ()

    def __init__(self, fpath, ):
        import csv

        self._fpath = fpath
        # store header of the data file
        with open(self._fpath, 'r', newline='') as _csv_fdata:
            self._csv_reader = csv.reader(_csv_fdata)
            self._data_header = next(self._csv_reader)

        # in-memory representation of data since it is not too heavy
        with open(self._fpath, 'r', newline='') as _csv_fdata:
            self._csv_dictreader = csv.DictReader(_csv_fdata)
            
            # _data_inm is a list with the following structure:
            # [dict({*param11*:*val11*, *param12*:*val12*, ...}, dict({*param21*:*val21*, *param22*:*val22*, ...})]
            self._data_inm = []
            for row in self._csv_dictreader:
                self._data_inm.append(row)

            self._id_max = int(self._data_inm[-1]['id'])

    def __repr__(self):
        return self._data_inm

    @property
    def data(self):
        return self._data_inm

    @data.setter
    def data(self):
        print(f'use obj_name.append_entry method to add new row to the db.')

    @data.deleter
    def data(self):
        raise AttributeError('Can not access this method.')

    def glimpse(self):
        return self._data_header
    
    def get_param(self, indep_params, dep_param='price_doc'):
        """
        Expects name of the parameter to be fetched (*dep_param*), 
        the *indep_params* (a dict with *param*:*value* pairs) with values to be tested against.
        Returns a result dict with *id*:*indep_param* pairs.
        """
        result_dict = {}

        for dict_line in self._data_inm:
            # test if all cols in a dict_line have desired values 
            if all(dict_line[k]==v for k, v in indep_params.items()):
                # TODO add explicit type conversion logic based on input param  
                result_dict[dict_line['id']] = int(dict_line[dep_param])
    
        return result_dict
        

    def append_entry(self, param_dict: Dict[str, str]):
        """
        Expected a dict of pairs *param*: *value*
        """
        import csv
        with open(self._fpath, 'a', newline='') as _csv_fdata:
            # TODO do not allow the user to manually provide id 
            fieldnames = self._data_header
            writer = csv.DictWriter(_csv_fdata, fieldnames=fieldnames, restval='NA')
            
            self._id_max += 1
            param_dict['id'] = self._id_max
            writer.writerow(param_dict)

if __name__=="__main__":
    # print(Data_handler._id_max)
    # print(Data_handler._data_header)

    homer = Data_handler('housing_data/train.csv')

    # for elem in homer.glimpse():
    #     print(elem)

    input_params = {'product_type':'Investment', 'sub_area':'Vnukovo', 'num_room':'2'}