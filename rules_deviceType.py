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
    laptop_rule = (df['model'] == 'macBook') | (df['os'] == 'Windows') |(df['os'] == 'Linux') | (df['model'] == 'macBookPro') | df['user_agent'].str.contains('origin', na=False, case=False)  | df['user_agent'].str.contains('laptop', na=False, case=False) 
    df.loc[laptop_rule, 'deviceType'] = 'Laptop'
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



