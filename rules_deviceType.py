import requests
import json
import pandas as pd
import pickle
import os
import helper
import config


def mark_deviceType_mobile(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tablet_rule = (df['model'].str.contains('tab', na= False, case = False) | df['model'].str.contains('ipad', na= False, case = False) |
                   df['model'].str.contains('mediapad', na= False, case = False))
    mobile_rule = (df['os'] == 'iOS') |((~tablet_rule) & (df['os'] == 'Android'))|(df['model'] == 'Galaxy')
    df.loc[mobile_rule, 'deviceType'] = 'Mobile'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_pc(write_to_file=True):
    df = helper.get_df(config._didbName_)
    laptop_rule = ((df['model'] == 'macBook') | (df['model'] == 'mac') | (df['os'] == 'Windows') |
        (df['os'] == 'Linux') | (df['model'] == 'macBookPro') | (df['model'] == "ThinkPad") |
        df['user_agent'].str.contains('origin', na=False, case=False) |
        df['user_agent'].str.contains('laptop', na=False, case=False) |
        df['user_agent'].str.contains('postman', na=False, case=False) |
        df['user_agent'].str.contains('curl', na=False, case=False))
    df.loc[laptop_rule, 'deviceType'] = 'PC'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_gamingConsole(write_to_file=True):
    df = helper.get_df(config._didbName_)
    gamingConsole_rule = ((df['model'] == 'Nintendo 3DS') | (df['model'] == 'PS5') | (df['model'] == 'Xbox') |
        (df['model'].str.contains('playstation', na=False, case=False)))
    df.loc[gamingConsole_rule, 'deviceType'] = 'Gaming Console'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_tv(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tv_rule = (df['model'].str.contains('tv', na=False, case = False))
    df.loc[tv_rule, 'deviceType'] = 'Smart TV'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_tablet(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tablet_rule = (df['model'].str.contains('tab', na= False, case = False) | df['model'].str.contains('ipad', na= False, case = False) |
                   df['model'].str.contains('mediapad', na= False, case = False))
    df.loc[tablet_rule, 'deviceType'] = 'Tablet'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_homeDevice(write_to_file=True):
    df = helper.get_df(config._didbName_)
    mobile_rule = (df['brand'].str.contains('Technicolor CH USA Inc.', na= False, case = False))
    df.loc[mobile_rule, 'deviceType'] = 'HomeDevice'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_VR(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tv_rule = (df['model'].str.contains('Quest', na=False, case = False))
    df.loc[tv_rule, 'deviceType'] = 'VR Headset'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_watch(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tv_rule = (df['model'].str.contains('watch', na=False, case = False))
    df.loc[tv_rule, 'deviceType'] = 'Watch'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_printer(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tv_rule = (df['model'].str.contains('printer', na=False, case = False))
    df.loc[tv_rule, 'deviceType'] = 'Printer'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_router(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tv_rule = (df['vendor'].str.contains('router', na=False, case = False))
    df.loc[tv_rule, 'deviceType'] = 'Router'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_deviceType_switch(write_to_file=True):
    df = helper.get_df(config._didbName_)
    tv_rule = (df['vendor'].str.contains('switch', na=False, case = False))
    df.loc[tv_rule, 'deviceType'] = 'Switch'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df