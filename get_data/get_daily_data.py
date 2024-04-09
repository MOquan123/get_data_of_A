import pandas as pd
import os
import baostock as bs
from datetime import datetime, timedelta

def get_daily_data(code_name_dict, period=60):
    # Determine the start and end date based on the period
    start_date = (datetime.today() - timedelta(days=period)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')

    data_folder = 'output/d_data'

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f'Folder {data_folder} created.')
    else:
        print(f'Folder {data_folder} already exists.')

    # Fetch and save the historical data for each stock
    for code, name in code_name_dict.items():
        # Fetch the historical data using baostock's query_history_k_data_plus function
        print(f"Fetching data for {code}:{name}")

        rs = bs.query_history_k_data_plus(
            code,  # use variable 'code' here
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg",
            start_date=start_date, end_date=end_date,
            frequency='d', adjustflag="3"
        )
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        df = pd.DataFrame(data_list, columns=rs.fields)

        print(f'Data for {code}:{name}:')
        print(df.head())
        if df.empty:
            continue
        df.to_csv(f'{data_folder}/{code}_{name}.csv')
