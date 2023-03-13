import requests
import json
import pandas as pd
import pickle
import os
import helper


def mark_deviceType_mobile(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    mobile_rule = (df['os'] == 'iOS') | (df['os'] == 'Android')|(df['model'] == 'Galaxy')
    df.loc[mobile_rule, 'deviceType'] = 'Mobile'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_deviceType_laptop(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    laptop_rule = ((df['model'] == 'macBook') | (df['os'] == 'Windows') |
        (df['os'] == 'Linux') | (df['model'] == 'macBookPro') |
        df['user_agent'].str.contains('origin', na=False, case=False) |
        df['user_agent'].str.contains('laptop', na=False, case=False) |
        df['user_agent'].str.contains('postman', na=False, case=False) |
        df['user_agent'].str.contains('curl', na=False, case=False))
    df.loc[laptop_rule, 'deviceType'] = 'PC'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_deviceType_gamingConsole(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    gamingConsole_rule = (df['model'] == 'Nintendo 3DS') | (df['model'] == 'PS5')
    df.loc[gamingConsole_rule, 'deviceType'] = 'Gaming Console'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_deviceType_tv(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    tv_rule = (df['model'].str.contains('tv', na=False, case = False))
    df.loc[tv_rule, 'deviceType'] = 'Smart TV'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_deviceType_tablet(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    mobile_rule = (df['model'].str.contains('tab', na= False, case = False))
    df.loc[mobile_rule, 'deviceType'] = 'Tablet'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_deviceType_homeDevice(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    mobile_rule = (df['brand'].str.contains('Technicolor CH USA Inc.', na= False, case = False))
    df.loc[mobile_rule, 'deviceType'] = 'HomeDevice'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df



