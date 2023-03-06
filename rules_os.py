import requests
import json
import pandas as pd
import pickle
import os
import helper

def mark_os_iphone(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    ios_rule = (df['brand'] == 'Apple') & ((df['model'].str.contains('iphone', na=False, case=False)))
    df.loc[ios_rule, 'os'] = 'iOS'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_os_mac(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    macos_rule = (df['brand'] == 'Apple') & ((df['model'].str.contains('mac', na=False, case=False)))
    df.loc[macos_rule, 'os'] = 'macOS'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_os_android(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    android_rule = (df['user_agent'].str.contains('android', na=False, case=False)) | (df['vendor'].str.contains('android', na=False, case=False))
    df.loc[android_rule, 'os'] = 'Android'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_os_windows(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    windows_rule = (df['user_agent'].str.contains('microsoft-wns', na=False, case=False)) | (df['user_agent'].str.contains('Microsoft-CryptoAPI', na=False, case=False))
    df.loc[windows_rule, 'os'] = 'Windows'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_os_linux(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    linux_rule = (df['user_agent'].str.contains('linux', na=False, case=False)) & (~df['user_agent'].str.contains('android', na=False, case=False))
    df.loc[linux_rule, 'os'] = 'Linux'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df