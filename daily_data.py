import pandas as pd
import os
import baostock as bs
import akshare as ak
from datetime import datetime, timedelta

# Determine the directory to save the data files
parent_folder = 'data'

def get_weekly_data(code_name_dict, weeks=60):
    # Determine the start and end date based on the period
    start_date = (datetime.today() - timedelta(weeks==weeks)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')

    data_folder = 'w_data'

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f'Folder {data_folder} created.')
    else:
        print(f'Folder {data_folder} already exists.')


    # Fetch and save the historical data for each stock
    for code, name in code_name_dict.items():
        if code.startswith(('sh', 'sz')):
            pass
        elif len(code) == 6:
            code = ('sh' if code.startswith('6') else 'sz') + '.' + code
        else:continue # 非标准的代码忽略

        if "*ST" in name or "ST" in name:
            continue  # skip special treatment (ST) stocks
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        print(f"Fetching data for {code}:{name}")

        # Fetch the historical data using baostock's query_history_k_data_plus function
        rs = bs.query_history_k_data_plus(
            code,  # use variable 'code' here
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg",
            start_date=start_date, end_date=end_date,
            frequency='w', adjustflag="3"
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

def get_daily_data(code_name_dict, period=60):
    # Determine the start and end date based on the period
    start_date = (datetime.today() - timedelta(days=period)).strftime('%Y-%m-%d')
    end_date = datetime.today().strftime('%Y-%m-%d')

    data_folder = 'd_data'

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f'Folder {data_folder} created.')
    else:
        print(f'Folder {data_folder} already exists.')


    # Fetch and save the historical data for each stock
    for code, name in code_name_dict.items():
        if code.startswith(('sh', 'sz')):
            pass
        elif len(code) == 6:
            code = ('sh' if code.startswith('6') else 'sz') + '.' + code
        else:continue # 非标准的代码忽略

        if "*ST" in name or "ST" in name:
            continue  # skip special treatment (ST) stocks
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        print(f"Fetching data for {code}:{name}")

        # Fetch the historical data using baostock's query_history_k_data_plus function
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

def init_data():
    # Log in to baostock
    lg = bs.login()
    # Getting the list of stock codes and names
    stock_df = ak.stock_zh_a_spot_em()
    # Filtering out the suspended and delisted stocks
    stock_df = stock_df[stock_df['最新价'] != '0.000']
    stock_df = stock_df[stock_df['最新价'] != '停牌']
    
    code_name_dict = stock_df.set_index('代码')['名称'].to_dict()
    get_daily_data(code_name_dict, 60)
    get_daily_data(code_name_dict, 60)

    bs.logout()

init_data()
