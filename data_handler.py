"""
Provides access to the Data_handler class, which is basically a general-purpose wrapper around a db file
with the following core self-explanatory methods of interest: 
    1. fetch_param(self, dependent_param, independent_param, value);
    2. append_entry(self, param_dict);
"""

class Data_handler:
    """
    Initializes object of Data_handler type.
    Expects path to a data file as an initialization input param.
    Data_handler obj allows storing data files in-memory, fetch data based on provided params, put data into a db file.   
    """
    def __init__(self, fpath):
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

            self._id_max = self._data_inm[-1]['id']

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
    
    def fetch_param(self, independent_param, value, dependent_param='price_doc'):
        """
        Expects name of the parameter to be fetched (*dependent_param*), 
        the *value* for *independent_param* to be tested against.,
        """
        result_list = [dict_line[dependent_param] for dict_line in self._data_inm if dict_line[independent_param] == value]
        try:
            avg_indep_param = sum(result_list)/len(result_list)
            print(f"""
            There are {len(result_list)} lines with {independent_param}={value}. 
            Avg price is {avg_indep_param}.""")
        except ZeroDivisionError:
            print(f'No lines with {independent_param}={value}')
            

            

    def append_entry(self, param_dict):
        """
        Expected a dict of pairs *param*: *value*
        """
        pass

# print(Data_handler._id_max)
# print(Data_handler._data_header)

homer = Data_handler('housing_data/train.csv')

for elem in homer.glimpse():
    print(elem)

print(homer.fetch_param('big_church_count_3000', 2))