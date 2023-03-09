import requests
import json
import pandas as pd
import pickle
import os
import helper, fetcher
import generate
import rules
import analytics

didbName = 'didb'

# 1 #
# fetcher.get_data(type='ALL')
# 2 #
# df = generate.create_didb()
# 3 #
# df = generate.populate_didb(didbName, 'ALL')

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
analytics.analyze_didb(didbName, False)

# print(df['user_agent'])
# for d in df['user_agent']:
#     parsed = helper.parse_useragent(d)
#     print(parsed)


# print(df[df['gw_mac'] == 'ec:c0:1b:65:f3:cc'])
# print(df[df['brand'] == 'Samsung'])
# print(df[df['mac'] == 'a830bcb40b6d']['user_agent'].to_string())
