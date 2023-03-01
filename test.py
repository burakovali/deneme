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


generate.create_didb()

df = generate.populate_didb(didbName, 'ALL')

df = helper.get_df(didbName)
helper.write_df_to_csv(df, 'processed_didb.csv')

# print(df[df['gw_mac'] == 'ec:c0:1b:65:f3:cc'])
# print(df[df['brand'] == 'Samsung'])
# print(df[df['mac'] == 'a830bcb40b6d']['user_agent'].to_string())
