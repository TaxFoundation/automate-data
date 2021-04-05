import json
import requests
import pprint
import pandas as pd
import time
import fed_data_api as fed

KEY = 'd87219606729528c27784921b44c5630'
BASE_URL = 'https://api.stlouisfed.org/fred/'

pp = pprint.PrettyPrinter()


def remove_pre_1960():
    # Remove everything pre-1960
    fed_df = pd.read_csv('output_fed_merge.csv')
    fed_df = fed_df[fed_df.date >= 1960]
    fed_df.to_csv('output_fed_merge.csv', index=False)


def append_observation(fed_data, id, index):
    # print(index)
    obj = fed.get_observation(id)
    # metadata = fed.get_series(id)
    # pp.pprint(metadata)
    # print(id)
    obj = obj['observations']
    # pp.pprint(obj)

    temp_df = pd.DataFrame()
    temp_values = []
    temp_dates = []
    series_name = []
    account = []
    var_number = []
    var_name = []
    proposed_var_name = []
    fed_unit = []
    fed_multiplier = []
    currency = []
    fed_unique_id = []

    df = pd.read_csv('fed_variable_key.csv')
    temp_series_name = df['FED Series Name'][index]
    temp_account = df['Account'][index]
    temp_var_number = df['Variable Number'][index]
    temp_var_name = df['Variable Name'][index]
    temp_proposed_var_name = df['Proposed variable name'][index]
    temp_fed_unit = df['FED Unit'][index]
    temp_fed_multiplier = df['FED Multiplier'][index]
    temp_currency = df['Currency'][index]
    temp_fed_unique_id = df['FED Unique Identifier'][index]

    # Create temporary lists of values and dates
    for i in obj:
        temp_values.append(i['value'])
        temp_dates.append(i['date'])
        series_name.append(temp_series_name)
        account.append(temp_account)
        var_number.append(temp_var_number)
        var_name.append(temp_var_name)
        proposed_var_name.append(temp_proposed_var_name)
        fed_unit.append(temp_fed_unit)
        fed_multiplier.append(temp_fed_multiplier)
        currency.append(temp_currency)
        fed_unique_id.append(temp_fed_unique_id)


    # Extract only the year from the date.
    for i, x in enumerate(temp_dates):
        temp_dates[i] = x[0:4]

    temp_df['series_name'] = series_name
    temp_df['Account'] = account
    temp_df['Variable Name'] = var_name
    temp_df['Proposed variable name'] = proposed_var_name
    temp_df['FED Unit'] = fed_unit
    temp_df['FED Multiplier'] = fed_multiplier
    temp_df['Currency'] = currency
    temp_df['FED Unique Identifier'] = fed_unique_id
    temp_df['date'] = temp_dates
    temp_df['value'] = temp_values

    fed_data = fed_data.append(temp_df)
    # print(id, fed_data)

    # Need the sleep otherwise it fails, might be another throttling issue.
    time.sleep(2)
    return fed_data


def fix_data_multiple():
    df = pd.read_csv('output_fed_merge.csv')
    df['value'] = df['value']/1000
    df.to_csv('output_fed_merge.csv', index=False)


def main():
    mapping = pd.read_csv('map_name_to_id.csv')
    series_ids = mapping['Series ID'].tolist()
    print(series_ids)

    fed_key_merged = pd.DataFrame()

    for i, x in enumerate(series_ids):
        fed_key_merged = append_observation(fed_key_merged, x, i)
        # metadata = parse_metadata(x)

    # print(fed_key_merged)
    fed_key_merged.to_csv('output_fed_merge.csv', index=False)
    remove_pre_1960()
    fix_data_multiple()
    print(fed_key_merged)


if __name__ == '__main__':
    main()
