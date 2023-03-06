import requests
import json
import pandas as pd
import pickle
import os
import helper


def mark_ios_version(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[df['os'] == 'iOS'].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            idx = -1
            ua_list = v['user_agent'].split()
            for iua,vua in enumerate(ua_list):
                if vua == 'os':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx]
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix]
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_android_version(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[df['os'] == 'Android'].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            idx = -1
            ua_list = v['user_agent'].split()
            for iua,vua in enumerate(ua_list):
                if "Android" in vua:
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx]
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix].split(";")[0]
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_windows_version(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    for i,v in df[df['os'] == 'Windows'].iterrows():
        if 'Microsoft-CryptoAPI' in v["user_agent"]:
            v["user_agent"].split('/')[1]
            df.loc[i, 'osVersion'] = v["user_agent"].split('/')[1]
        elif 'Microsoft-WNS' in v["user_agent"]:
            v["user_agent"].split('/')[1]
            df.loc[i, 'osVersion'] = v["user_agent"].split('/')[1]
    if write_to_file:
        helper.update_didb(df, didbName)
    return df
    