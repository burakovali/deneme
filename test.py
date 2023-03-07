import requests
import json
import pandas as pd
import pickle
import os
import helper, fetcher
import generate
import rules

didbName = 'didb'

# fetcher.get_data(type='ALL')

# generate.create_didb()
df = generate.populate_didb(didbName, 'ALL')

# create os-parameters lists for known devices
df = generate.os_params_list(didbName, False)
helper.write_df_to_csv(df, 'os_param_list.csv')

df = helper.get_df(didbName)
helper.write_df_to_csv(df, 'processed_didb.csv')

df = generate.merge_didb(didbName, True)
helper.write_df_to_csv(df, 'merged_didb.csv')



# print(df['user_agent'])
# for d in df['user_agent']:
#     parsed = helper.parse_useragent(d)
#     print(parsed)


# print(df[df['gw_mac'] == 'ec:c0:1b:65:f3:cc'])
# print(df[df['brand'] == 'Samsung'])
# print(df[df['mac'] == 'a830bcb40b6d']['user_agent'].to_string())
