import requests
import json
import pandas as pd
import pickle
import os, re
import helper, fetcher
import generate
import rules
import analytics, query

didbName = 'didb'
ouiName = 'oui'
# 1 #
# fetcher.get_data(type='ALL')
# 2 #
# df = generate.create_didb()
#df_oui = generate.get_ouiList()
# 3 #
df = generate.populate_didb(didbName, 'ALL', True)

# create os-parameters lists for known devices
""" df_param = generate.os_params_list(didbName, False)
helper.write_df_to_csv(df_param, 'os_param_list.csv') """

# 4 #
# df = helper.get_df(didbName)
# helper.write_df_to_csv(df, 'processed_didb.csv')

# 5 #
# df = generate.merge_didb(didbName, True)
# helper.write_df_to_csv(df, 'merged_didb.csv')

# 6 #
# analytics.analyze_didb(didbName, False)

# 7 #
# analytics.count_missing_values(didbName, False)


# 8 #
# query.query_by_mac(didbName, '78:4f:43:a0:98:72')
# query.query_by_brand(didbName, 'apple')
# query.query_by_model(didbName, 'iphone')

# print(df['user_agent'])
# for d in df['user_agent']:
#     parsed = helper.parse_useragent(d)
#     print(parsed)


# print(df[df['gw_mac'] == 'ec:c0:1b:65:f3:cc'])
# print(df[df['brand'] == 'Samsung'])
# print(df[df['mac'] == 'a830bcb40b6d']['user_agent'].to_string())
