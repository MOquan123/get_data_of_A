# import baostock as bs
# import pandas as pd
# from datetime import datetime, timedelta

# def get_weekly_data(stock_code, weeks=60):
#     # Log in to baostock
#     lg = bs.login()

#     # Calculate the start and end dates for the past weeks
#     end_date = datetime.today().strftime('%Y-%m-%d')
#     start_date = (datetime.today() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')

#     # Query for the historical k-line data
#     rs = bs.query_history_k_data_plus(
#         stock_code,
#         "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
#         start_date=start_date,
#         end_date=end_date,
#         frequency="w",  # use "w" for weekly data
#         adjustflag="3"  # "3" for no adjust
#     )

#     # Save the data into a Pandas DataFrame
#     data_list = []
#     while (rs.error_code == '0') & rs.next():
#         data_list.append(rs.get_row_data())
#     df = pd.DataFrame(data_list, columns=rs.fields)
    
#     # Logout from baostock
#     bs.logout()
    
#     return df

# # Test the function
# stock_code = "sh.600000"
# df = get_weekly_data(stock_code, weeks=60)
# print(df)