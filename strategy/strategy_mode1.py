import pandas as pd
import os

def strategy_mode1():
    # Get the falling dates for the SH index
    df = pd.read_csv('output/sh.000001_上证指数.csv')
    fall_dates = sorted(set(df[df['pctChg'] < 0]['date']))  

    # Getting all the csv files in d_data directory that starts with 'sh'
    file_path = 'output/d_data/'
    file_list = [f for f in os.listdir(file_path) if f.endswith('.csv') and f.startswith('sh')]

    for fall_date in fall_dates:
        rise_stock_count = 0  
        rise_next_day_count = 0  

        for file in file_list:
            # Read the stock data
            stock_df = pd.read_csv(f'{file_path}{file}')
            stock_df['date'] = pd.to_datetime(stock_df['date'])

            # Check if this stock rises on this falling date
            stock_rise_mask = (stock_df['date'] == fall_date) & (stock_df['pctChg'] > 0)

            if stock_rise_mask.any():
                rise_stock_count += 1  

                # Find the index of the rising date
                rise_index = stock_df.index[stock_rise_mask][0]
                # Check if this stock rises the next day
                if rise_index < len(stock_df) - 1:  # ensure we don't exceed the DataFrame's bounds
                    stock_rise_next_day = stock_df.loc[rise_index + 1]
                    if stock_rise_next_day['pctChg'] > 0:
                        rise_next_day_count += 1  

        print(f"On date {fall_date}, {rise_stock_count} stocks rose while the SH index fell.")
        if rise_stock_count > 0:
            probability = rise_next_day_count / rise_stock_count
            print(f"The probability that these stocks continue to rise the next day is {probability*100} %.")  
        else:
            print("No stock rose while the SH index fell on this day.")

# strategy_mode1()