import requests
import json
import pandas as pd
import pickle
import os
import helper

def mark_os_iphone(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    #ios_rule = (df['brand'] == 'Apple') & ((df['model'].str.contains('iphone', na=False, case=False)))
    
    ios_rule = (
        # read ios from user agent
        df['user_agent'].str.contains("ios", na=False, case = False) |
        df['user_agent'].str.contains("iphone.OS", regex = True, na=False, case = False) |
        # infer from model
        df['model'].str.contains('iphone', na=False, case=False)
    )

    df.loc[ios_rule, 'os'] = 'iOS'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_os_mac(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    # macos_rule = (df['brand'] == 'Apple') & ((df['model'].str.contains('mac', na=False, case=False)))
    macos_rule = (
        df['model'].str.contains('mac', na=False, case=False)
    )
    df.loc[macos_rule, 'os'] = 'macOS'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df



def mark_os_windows(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    windows_rule = (df['user_agent'].str.contains('microsoft-wns', na=False, case=False)) | (df['user_agent'].str.contains('microsoft', na=False, case=False)) | (df['user_agent'].str.contains('Microsoft-CryptoAPI', na=False, case=False)) | (df['vendor'].str.contains('MSFT', na=False, case=False))
    df.loc[windows_rule, 'os'] = 'Windows'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_os_linux(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    # linux_rule = (df['user_agent'].str.contains('linux', na=False, case=False)) & (~df['user_agent'].str.contains('android', na=False, case=False))
    linux_rule = (
        # read from hostname, user agent or vendor but there must not be 'android'
        df['hostname'].str.contains('linux', na=False, case=False) |
        df['vendor'].str.contains('linux', na=False, case=False) |
        df['user_agent'].str.contains('linux', na=False, case=False) |
        df['user_agent'].str.contains('Debian', na=False, case=False) |
        df['hostname'].str.contains('X11', na=False, case=False) |
        df['vendor'].str.contains('X11', na=False, case=False) |
        df['user_agent'].str.contains('X11', na=False, case=False) |
        df['hostname'].str.contains('ubuntu', na=False, case=False) |
        df['vendor'].str.contains('ubuntu', na=False, case=False) |
        df['user_agent'].str.contains('ubuntu', na=False, case=False)
    )
    linux_rule = linux_rule & (~df['user_agent'].str.contains('android', na=False, case=False))
    df.loc[linux_rule, 'os'] = 'Linux'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_os_android(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    #android_rule = (df['user_agent'].str.contains('android', na=False, case=False)) | (df['vendor'].str.contains('android', na=False, case=False))
    android_rule = (
        # read from hostname, user agent or vendor
        df['hostname'].str.contains('android', na=False, case=False) |
        df['vendor'].str.contains('android', na=False, case=False) |
        df['user_agent'].str.contains('android', na=False, case=False) |
        # infer from model
        df['model'].str.contains('galaxy', na=False, case=False) 
        # type is mobile and brand is not apple
        # ((df['type'].str.contains('Mobile')) & (df['brand']!= 'Apple') & (df['brand']!=''))
    )
    df.loc[android_rule, 'os'] = 'Android'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_os_nintendo3SDSS(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    # android_rule = (df['user_agent'].str.contains('android', na=False, case=False)) | (df['vendor'].str.contains('android', na=False, case=False))
    
    nintendoOS_rule = (
        # infer from model
        df['model'].str.contains('nintendo 3ds', na=False, case=False)
    )
    
    df.loc[nintendoOS_rule, 'os'] = 'Nintendo 3DS System Software'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_os_ipad(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    # android_rule = (df['user_agent'].str.contains('android', na=False, case=False)) | (df['vendor'].str.contains('android', na=False, case=False))
    apple_tablet_rule= False
    if 'type' in df.index:
        apple_tablet_rule = ((df['type'].str.contains('tablet', na=False, case=False)) & (df['brand']=='Apple'))

    ipadOS_rule = (
        # infer from model
        df['model'].str.contains('ipad', na=False, case=False) |
        # tablet type and apple brand
        apple_tablet_rule
    )
    
    df.loc[ipadOS_rule, 'os'] = 'iPadOS'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

 
def mark_os_unix(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    # android_rule = (df['user_agent'].str.contains('android', na=False, case=False)) | (df['vendor'].str.contains('android', na=False, case=False))
    
    unix_rule = (
        # read from user agent or vendor
        df['vendor'].str.contains('udhcp', na=False, case=False)
    )
    
    df.loc[unix_rule, 'os'] = 'UNIX'
    if write_to_file:
        helper.update_didb(df, didbName)
