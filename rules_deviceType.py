import requests
import json
import pandas as pd
import pickle
import os
import helper


def mark_deviceType_mobile(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    mobile_rule = (df['OS'] == 'iOS') | (df['model'] == 'Galaxy')
    df.loc[mobile_rule, 'type'] = 'Mobile'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_deviceType_laptop(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    laptop_rule = (df['model'] == 'macBook') | (df['model'] == 'macBookPro')
    df.loc[laptop_rule, 'type'] = 'Laptop'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_deviceType_gamingConsole(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    gamingConsole_rule = (df['model'] == 'Nintendo 3DS') | (df['model'] == 'PS5')
    df.loc[gamingConsole_rule, 'type'] = 'Laptop'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df
    