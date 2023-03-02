import requests
import json
import pandas as pd
import pickle
import os
import helper
    

def mark_modelVersion_galaxy(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'Galaxy')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            idx = -1
            ua_list = v['hostname'].split('-')
            for iua,vua in enumerate(ua_list):
                if vua == 'Galaxy':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx]
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'model_version'] = version_list[ix]

    galaxy_rule_A11 = (df['brand'] == 'Samsung') & (df['user_agent'].str.contains('SM-A115F', na=False, case=True))
    df.loc[galaxy_rule_A11, 'model_version'] = 'A11'

    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_modelVersion_galaxyTab(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'GalaxyTab')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            idx = -1
            ua_list = v['hostname'].split('-')
            for iua,vua in enumerate(ua_list):
                if vua == 'Tab':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx]
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'model_version'] = version_list[ix]
    
    galaxyTab_rule_S6 = (df['brand'] == 'Samsung') & (df['user_agent'].str.contains('SM-P610', na=False, case=True))
    df.loc[galaxyTab_rule_S6, 'model_version'] = 'S6'

    if write_to_file:
        helper.update_didb(df, didbName)
    return df

