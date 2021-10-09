import csv

def fetch_price(param_name, value):
    """
    Expected name of the parameter and its corresponding value for rows to be tested against.
    Possibly will be reorganised into a class to hold temporary values when the architecture is decided on.
    """
    pass

    with open('housing_data/train.csv', 'r', newline='') as csv_fdata:
        csv_reader = csv.DictReader(csv_fdata)
        line_count = 0
        price_list = []
        for row in csv_reader:
            if line_count == 0:
                header = row
            
            if row[param_name] == value:
                price_list.append(row['price_doc'])
            line_count += 1
    # print(f'Processed {line_count} lines.')
    return price_list

def put_data(param_dict):
    """expected a dict of pairs *param*: *value*"""
    pass

    with open('housing_data/train.csv', 'a', newline='') as csv_fdata:
        csv_writer = csv.DictWriter(csv_fdata)
        csv_writer.writerow(param_dict)