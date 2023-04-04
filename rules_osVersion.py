import requests
import json
import pandas as pd
import pickle
import os
import helper
import config


def mark_modelVersion_appleOS_generic(write_to_file=True):
    df = helper.get_df(config._didbName_)
    idx_list = []
    version_list = []
    for i,v in df[(df['brand'] == 'Apple')].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            idx = -1
            ua_list = v['user_agent'].split('/')
            for iua,vua in enumerate(ua_list):
                if 'Version' in vua:
                    idx = iua + 1
                    break
            if idx != -1:
                myversion = ua_list[idx].split()[0]
        if myversion is not None:
            knownVersion = v['osVersion']
            if knownVersion != knownVersion :
                knownVersion = str(0)
            # print(str(knownVersion) + ' - ' + str(myversion))
            f_myversion = myversion.replace(".", "")
            f_knownVersion = knownVersion.replace(".", "")
            if f_knownVersion < f_myversion:
                idx_list.append(i)
                version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix]

    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_ios_version(write_to_file=True):
    df = helper.get_df(config._didbName_)
    idx_list = []
    version_list = []
    for i,v in df[df['os'] == 'iOS'].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            idx = -1
            ua_list = v['user_agent'].split()
            for iua,vua in enumerate(ua_list):
                if vua == 'OS':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = str(ua_list[idx])
        if myversion is not None:
            idx_list.append(i)
            myversion = myversion.replace("_", ".")
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix]
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_macos_version(write_to_file=True):
    df = helper.get_df(config._didbName_)
    idx_list = []
    version_list = []
    for i,v in df[df['os'] == 'macOS'].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            idx = -1
            ua_list = v['user_agent'].split()
            for iua,vua in enumerate(ua_list):
                if vua == 'OS':
                    idx = iua + 2
                    break        
            if idx != -1:
                myversion = str(ua_list[idx][:-1])
        if myversion is not None:
            idx_list.append(i)
            myversion = myversion.replace("_", ".")
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix]
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_macos_from_userAgent (write_to_file=True):
    df = helper.get_df(config._didbName_)
    df.loc[df['model'].str.contains('Darwin/22.2.0', na=False, case = False), 'osVersion'] = '12.2'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_appleOS_version_userAgent(write_to_file=True):
    df = helper.get_df(config._didbName_)
    idx_list = []
    version_list = []
    for i,v in df[(df['user_agent'].str.contains('invitation-registration', na=False, case=False))].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            my_ua = v['user_agent']
            myversion= my_ua[my_ua.find('['):my_ua.find(']')].split(',')[1]
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix]
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_android_version(write_to_file=True):
    df = helper.get_df(config._didbName_)
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
                myversion = ua_list[idx][:-1]
        if myversion is not None:
            if myversion.isdigit():
                idx_list.append(i) 
                version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix].split(";")[0]
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_android_version_oneday(write_to_file=True):
    df = helper.get_df(config._didbName_)
    idx_list = []
    version_list = []
    for i,v in df[df['os'] == 'Android'].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            idx = -1
            ua_list = v['user_agent'].split('/')
            for iua,vua in enumerate(ua_list):
                if "oneday" in vua:
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx][len(ua_list[idx])-1]
        if myversion is not None:
            if myversion.isdigit():
                idx_list.append(i) 
                version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'osVersion'] = version_list[ix].split(";")[0]
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df


def mark_windows_version(write_to_file=True):
    df = helper.get_df(config._didbName_)

    for i,v in df[df['os'] == 'Windows'].iterrows():
        if not pd.isna(v["user_agent"]):
            if 'Microsoft-CryptoAPI' in v["user_agent"]:
                v["user_agent"].split('/')[1]
                df.loc[i, 'osVersion'] = v["user_agent"].split('/')[1]
            elif 'Microsoft-WNS' in v["user_agent"]:
                v["user_agent"].split('/')[1]
                df.loc[i, 'osVersion'] = v["user_agent"].split('/')[1]
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df



def mark_linux_version(write_to_file=True):
    df = helper.get_df(config._didbName_)

    for i,v in df[df['os'] == 'Linux'].iterrows():
        if not pd.isna(v["user_agent"]):
            if 'Linux x86_64' in v["user_agent"]:
                df.loc[i, 'osVersion'] = '64 bit'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df