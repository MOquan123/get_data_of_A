import pandas as pd
import os
import baostock as bs
from datetime import datetime, timedelta

def get_index_daily_data(code, code_name, period=60):
    # Determine the start and end date based on the period
    start_date = (datetime.today() - timedelta(days=period)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')

    data_folder = 'output'

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f'Folder {data_folder} created.')
    else:
        print(f'Folder {data_folder} already exists.')

    # Fetch the historical data of the index
    print(f"Fetching data for {code}:{code_name}")

    rs = bs.query_history_k_data_plus(
        code,  # use 'code' here to get the index data
        "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg",
        start_date=start_date, end_date=end_date,
        frequency='d', adjustflag="3"
    )
    
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    df = pd.DataFrame(data_list, columns=rs.fields)

    print(f'Data for {code}:{code_name}:')
    print(df.head())
    if df.empty:
        return
    df.to_csv(f'{data_folder}/{code}_{code_name}.csv')
