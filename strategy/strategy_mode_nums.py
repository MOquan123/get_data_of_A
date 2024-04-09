
import pandas as pd
import os

price_diffs = []

import pandas as pd
import os

def search_stocks_by_volume(path,num_data=11):
    file_list = [f for f in os.listdir(path) if f.endswith('.csv')]
    target_stocks = []
    
    for file in file_list:
        df = pd.read_csv(os.path.join(path, file))
        df['volume'] = df['volume'].astype(float)
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)

        # Make sure we have at least 31 days of data
        if len(df) < num_data:
            continue
        
        # Calculate the highest price of past 30 trading days
        df['highest_past_30_days'] = df['high'].rolling(window=num_data).max().shift(1)

        # Check if the price drop is within 40%
        df['price_drop_within_40_percent'] = df['close'] < 0.6 * df['highest_past_30_days']

        # Get the volume of 10 days ago
        df['volume_10_days_ago'] = df['volume'].shift(11)

        # Find the dates where the volume is 75% less than the volume of 10 trading days ago
        # and the price drop is within 40%
        target_dates = df[(df['volume'] < 0.65 * df['volume_10_days_ago']) &((df['volume'] >= 0.25 * df['volume_10_days_ago']) )& df['price_drop_within_40_percent']]['date']
        
        if not target_dates.empty:
            # If found such date, store the stock file and the dates
            target_stocks.append((file, target_dates.tolist()))

    return target_stocks

# Then you can analyze the target stocks like before

def analyze_target_stocks(target_stocks, path):
    num_positive_diffs = 0  # 满足条件的股票数量
    total_diffs = 0  # 总的股票数量（处于target_stocks中的）
    
    num = 8
    for file, dates in target_stocks:
        df = pd.read_csv(os.path.join(path, file))
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)

        for date in dates:
            target_index = df[df['date'] == date].index[0]
            if target_index + num < len(df):
                total_diffs += 1
                close_price_diff = df.loc[target_index + num, 'close'] - df.loc[target_index, 'close']
                
                if close_price_diff > 0:
                    num_positive_diffs += 1 
                
                
                print(f"For stock {file}, on date {date}, the {num}-day price diff is: {close_price_diff}")
    
    
    if total_diffs > 0:
        probability = num_positive_diffs / total_diffs
        print(f"The probability that the close price is higher after {num} days is: {probability*100}%")
    else:
        print("No valid data for calculation.")

target_stocks = search_stocks_by_volume('output/d_data/')
analyze_target_stocks(target_stocks, 'output/d_data/')


