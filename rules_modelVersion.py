import requests
import json
import pandas as pd
import pickle
import os
import helper
import re
    

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
        df.loc[vx, 'modelVersion'] = version_list[ix]

    galaxy_rule_A11 = (df['brand'] == 'Samsung') & (df['user_agent'].str.contains('SM-A115F', na=False, case=True))
    galaxy_rule_S9plus = (df['brand'] == 'Samsung') & (df['user_agent'].str.contains('SM-G965F', na=False, case=True))

    df.loc[galaxy_rule_A11, 'modelVersion'] = 'A11'
    df.loc[galaxy_rule_S9plus, 'modelVersion'] = 'S9+'

    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_modelVersion_appleUserAgent(didbName='didb', write_to_file=True):
    print("apple model version start")
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['user_agent'].str.contains('invitation-registration', na=False, case=False))].iterrows():
        print("apple model version row", i)
        myversion = None
        if not pd.isna(v['user_agent']):
            my_ua = v['user_agent']
            s= my_ua[my_ua.find('['):my_ua.find(']')].split(',')[3]
            myversion = re.match(r'([a-zA-Z]+)(\d+)', s).group(2) #iphone10 --> 10
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'modelVersion'] = version_list[ix]

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
                if 'lite' in v['hostname']:
                    myversion += " Lite"
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'modelVersion'] = version_list[ix]
    
    galaxyTab_rule_S6 = (df['brand'] == 'Samsung') & (df['user_agent'].str.contains('SM-P610', na=False, case=True))
    df.loc[galaxyTab_rule_S6, 'modelVersion'] = 'S6 Lite'

    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_modelVersion_mediaPad(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'MediaPad')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            # print("MediaPad vers")
            idx = -1
            ua_list = v['hostname'].split('_')
            for iua,vua in enumerate(ua_list):
                if vua == 'MediaPad':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx] + ' ' + ua_list[(idx+1)] + ' ' + ua_list[(idx+2)]
        if myversion is not None:
            # print("MediaPad", myversion)
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'modelVersion'] = version_list[ix]
    
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_modelVersion_ThinkPad(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'ThinkPad')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            idx = -1
            ua_list = v['hostname'].split('-')
            for iua,vua in enumerate(ua_list):
                if vua == 'ThinkPad':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx]
        if myversion is not None:
            # print("ThinkPad", myversion)
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        # print(myversion)
        df.loc[vx, 'modelVersion'] = version_list[ix]
    
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_modelVersion_xiaomiMi(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'Xiaomi-Mi')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            idx = -1
            ua_list = v['hostname'].split('-')
            for iua,vua in enumerate(ua_list):
                if vua == 'Mi':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx]
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'modelVersion'] = version_list[ix]
    
    MI8_rule = ((df['model'] == 'Xiaomi-Mi') & df['hostname'].str.contains("MI8") |
                (df['model'] == 'Xiaomi-Mi') & df['user_agent'].str.contains("MI 8") )
    df.loc[MI8_rule, 'modelVersion'] = '8'

    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_modelVersion_xiaomiRedmiNote(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    #from user agent
    idx_list = []
    version_list = []
    pattern = r"Redmi Note (\d+)\s+Pro"
    for i,v in df[(df['model'] == 'Redmi Note')].iterrows():
        myversion = None
        if not pd.isna(v['user_agent']):
            match = re.search(pattern, v['user_agent'])
            if match:
                myversion = match.group(1) + " pro"
        if myversion is not None:
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        df.loc[vx, 'modelVersion'] = version_list[ix]
    #from hostname
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'Redmi Note')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            idx = -1
            ua_list = v['hostname'].split('-')
            for iua,vua in enumerate(ua_list):
                if vua == 'Note':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx] + ' ' + ua_list[idx+1]
        if myversion is not None:
            # print("ThinkPad", myversion)
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        # print(myversion)
        df.loc[vx, 'modelVersion'] = version_list[ix]
    if write_to_file:
        helper.update_didb(df, didbName)
    return df



def mark_model_xboxOne(didbName='didb', write_to_file=True): #xbox one
    df = helper.get_df(didbName)

    xbox_rule = (
        (df['user_agent'].str.contains('xboxone', regex=False, na=False, case=False) |
         df['hostname'].str.contains('xboxone', regex=False, na=False, case=False))
    )
    
    df.loc[xbox_rule, 'modelVersion'] = 'Xbox One'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_modelVersion_huaweiP(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'Huawei-P')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            idx = -1
            ua_list = v['hostname'].split('_')
            for iua,vua in enumerate(ua_list):
                if vua == 'HUAWEI':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx]
                if 'lite' in v['hostname']:
                    myversion += " Lite"
        if myversion is not None:
            # print("ThinkPad", myversion)
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        # print(myversion)
        df.loc[vx, 'modelVersion'] = version_list[ix]
    
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_modelVersion_eliteBook(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    idx_list = []
    version_list = []
    for i,v in df[(df['model'] == 'EliteBook')].iterrows():
        myversion = None
        if not pd.isna(v['hostname']):
            idx = -1
            ua_list = v['hostname'].split('-')
            for iua,vua in enumerate(ua_list):
                if vua == 'EliteBook':
                    idx = iua + 1
                    break        
            if idx != -1:
                myversion = ua_list[idx] + ua_list[idx+1]
        if myversion is not None:
            # print("ThinkPad", myversion)
            idx_list.append(i)
            version_list.append(myversion)
    for ix, vx in enumerate(idx_list):
        # print(myversion)
        df.loc[vx, 'modelVersion'] = version_list[ix]
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_xiaomi_version_oneday(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
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
        df.loc[vx, 'modelVersion'] = version_list[ix].split(";")[0]
    if write_to_file:
        helper.update_didb(df, didbName)
    return df