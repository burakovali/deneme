import requests
import json
import pandas as pd
import pickle
import os
import helper
import config

def mark_model_mac(write_to_file=True):
    df = helper.get_df(config._didbName_)
    
    mac_rule = df['model'].isnull() & ((df['assoc_req_spatial_stream'] == 3) | df['os'].str.contains('mac', na=False, case=False) | (df['user_agent'].str.contains('macintosh', na=False, case=False)))

    df.loc[mac_rule, 'model'] = 'mac'

    df.loc[df['model'] == 'mac', 'os'] = 'macOS'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_pc(write_to_file=True):
    df = helper.get_df(config._didbName_)
    
    mac_rule = df['deviceType'].isnull() & (df['model'].str.contains('mac', na=False, case=False))

    df.loc[mac_rule, 'deviceType'] = 'PC'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df