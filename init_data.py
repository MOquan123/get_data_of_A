import pandas as pd
import os
import baostock as bs
import akshare as ak
from datetime import datetime, timedelta
from get_data.get_daily_data import get_daily_data
from get_data.get_weekly_data import get_weekly_data 
from get_data.get_monthly_data import get_monthly_data 
from get_data.get_index_daily_data import get_index_daily_data 



def init_data():
    # Log in to baostock

    output_folder = 'output'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f'Folder {output_folder} created.')
    else:
        print(f'Folder {output_folder} already exists.')

    lg = bs.login()
    stock_df = ak.stock_zh_a_spot_em()
    # Filtering out the suspended and delisted stocks
    stock_df = stock_df[stock_df['最新价'] != '0.000']
    stock_df = stock_df[stock_df['最新价'] != '停牌']

    code_name_dict = stock_df.set_index('代码')['名称'].to_dict()

    # Preprocess the code_name_dict
    processed_dict = {}

    for code, name in code_name_dict.items():
        if "*ST" in name or "ST" in name or "退市" in name:
            continue  # skip special treatment (ST) stocks
        if code.startswith(('sh', 'sz')):   # modified
            continue
        if code.startswith('6'):  
            pass
        elif code.startswith(('000', '001')): 
            pass
        else:
            continue  
        code = ('sh' if code.startswith('6') else 'sz') + '.' + code  # modified
        name = ''.join(c for c in name if c.isalnum() or c.isspace())
        processed_dict[code] = name

    if len(processed_dict) == 0:
        print(f'processed_dict is empty.')

            
    get_daily_data(processed_dict, 180)
    # get_weekly_data(processed_dict, 60)
    # get_monthly_data(processed_dict, 60)
    # get_index_daily_data('sh.000001', '上证指数',60)
    print(f'have been getting A nums is ' + str(len(processed_dict)))
    bs.logout()
