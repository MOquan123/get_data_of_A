import pandas as pd
import os
import baostock as bs
from datetime import datetime, timedelta

def get_monthly_data(code_name_dict, period=12):
    # Determine the start and end date based on the period
    start_date = (datetime.today() - timedelta(months=period)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    data_folder = 'output/m_data'

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f'Folder {data_folder} created.')
    else:
        print(f'Folder {data_folder} already exists.')

    # Fetch and save the historical data for each stock
    for code, name in code_name_dict.items():
        print(f"Fetching data for {code}:{name}")

        # Query for the historical k-line basic data
        rs = bs.query_history_k_data_plus(
            code,
            "date,code,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=end_date,
            frequency="m",  # use "m" for monthly data
            adjustflag="3"  # "3" for no adjust
        )
        
        if rs.error_code != '0':
            print(f'Failed to query history k data, error_msg: {rs.error_msg}')
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)
    
        print(f'Data for {code}:{name}:')
        print(df.head())
        if df.empty:
            continue
        df.to_csv(f'{data_folder}/{code}_{name}.csv')