import requests
import json
import pandas as pd
import pickle
import os, re
import helper, fetcher
import generate
import rules
import analytics, query
import cProfile

didbName = 'didb'
ouiName = 'oui'
# 1 #
myDate_after = '2023-03-22 14:00:00'
myDate_before = '2023-03-23 13:00:00'
dateInfo = {'use_timeRange': True, 'startDate': myDate_after, 'endDate': myDate_before, 'interval': '6h'}

# fetcher.get_data(dateInfo, type='ALL')
fetcher.get_data_intervals_recursive(dateInfo, type='ALL')

# 2 #
#df = generate.create_didb()
df = helper.read_pickle(didbName)
# 3 #
# df = generate.populate_didb(didbName, 'ALL', True)

# create os-parameters lists for known devices
""" df_param = generate.os_params_list(didbName, False)
helper.write_df_to_csv(df_param, 'os_param_list.csv') """

# 4 #
df = helper.get_df(didbName)
helper.write_df_to_csv(df, 'processed_didb.csv')

# 5 #
#df = generate.merge_didb(didbName, True)
#helper.write_df_to_csv(df, 'merged_didb.csv')

# 6 #
#analytics.analyze_didb(didbName, False)

# 7 #
#analytics.count_missing_values(didbName, False)


# 8 #
# query.query_by_mac(didbName, '78:4f:43:a0:98:72')
# query.query_by_brand(didbName, 'apple')
# query.query_by_model(didbName, 'iphone')
# query.query_by_params(didbName, '1-121-3-6-15-108-114-119-252')
# query.query_by_timestamp(didbName, '2023-03-10T10:41:04', '2023-03-11T10:41:04')
# query.query_by_gwmac(didbName, '00:1c:7f:81:58:27')

# print(df['user_agent'])
# for d in df['user_agent']:
#     parsed = helper.parse_useragent(d)
#     print(parsed)


# print(df[df['gw_mac'] == 'ec:c0:1b:65:f3:cc'])
# print(df[df['brand'] == 'Samsung'])
# print(df[df['mac'] == 'a830bcb40b6d']['user_agent'].to_string())
