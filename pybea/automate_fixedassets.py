import pybea
import pprint
import pandas as pd
import sys
import time
import pickle

# UserID = '1985ECDD-2CF4-4239-8A48-4C1C2FFA9A95'
UserID = 'AEC7FDB2-4F22-4296-982D-7CA35C0341BA'


def update_all_fa():
    pass


def update_fa(tablenames, frequency, year):
    failed_list = []
    mb_remaining = 100
    requests_remaining = 100

    for x in tablenames:
        print(x)
        try:
            temp = pybea.get_data(UserID, 'FixedAssets', TableName=x, Frequency='A', Year=year)
            # Compute how many megabytes each request is
            print('This request was ', sys.getsizeof(temp) / 1000000, 'megabytes')
            size = sys.getsizeof(temp) / 1000000
            mb_remaining -= size
            requests_remaining -= 1
            print('You have ', mb_remaining, 'more megabytes before throttling and ', requests_remaining,
                  'request/s remaining before throttling.')
            temp.to_csv('../FA_DATA/{0}.csv'.format(x))
            time.sleep(1)
            if mb_remaining < 5:
                time.sleep(30)
                mb_remaining = 100
            if requests_remaining < 2:
                time.sleep(45)
                requests_remaining = 100
        except KeyError:
            failed_list.append(x)
            print('Failure')
            time.sleep(.75)
    return failed_list


def main():
    print(pybea.get_data_set_list(UserID))
    print(pybea.get_parameter_list(UserID, 'FixedAssets'))
    fa_params = pybea.get_parameter_list(UserID, 'FixedAssets')


    fa_table_names = pybea.get_parameter_values(UserID, 'FixedAssets', ParameterName='TableName', ResultFormat='JSON')
    tablenames = fa_table_names['TableName'].values
    print(tablenames)

    # nipa_table_ids = pybea.get_parameter_values(UserID, 'FixedAssets', ParameterName='TableID', ResultFormat='JSON')
    fixed_assets = update_fa(tablenames, 'A', 2015)




if __name__ == '__main__':
    main()