import requests
import json
import pandas as pd
import pickle
import os
import helper
import config

params_android = ['1-3-6-15-26-28-51-58-59-43', '1-3-6-15-26-28-51-58-59-43-114-108']
params_ios = ['1-121-3-6-15-108-114-119-252', '1-121-3-6-15-114-119-252']
params_ipad = ['1-121-3-6-15-114-119-252']
params_macos = ['1-121-3-6-15-108-114-119-252-95-44-46', '1-121-3-6-15-114-119-252-95-44-46', '1-121-3-6-15-119-252-95-44-46']
params_unix = ['1-3-6-12-15-28-42-212', '1-3-6-12-15-28-42']
params_windows = ['1-3-6-15-31-33-43-44-46-47-119-121-249-252']
params_linux = ['1-2-6-12-15-26-28-121-3-33-40-41-42-119-249-252-17', '1-28-2-3-15-6-119-12-44-47-26-121-42-249-33-252']
# TODO: os rules for these following:
params_linux_debian = ['1-28-2-3-15-6-12']
params_embedded = ['1-3-6-28']
params_appletv = ['1-3-6-15-67-43-60']

def mark_os_appleTV(write_to_file=True):
    df = helper.get_df(config._didbName_)
    #option 55
    df.loc[df['params'].isin(params_appletv), 'os'] = 'Apple TV OS'

    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df


def mark_os_iphone(write_to_file=True):
    df = helper.get_df(config._didbName_)
    #ios_rule = (df['brand'] == 'Apple') & ((df['model'].str.contains('iphone', na=False, case=False)))
    
    ios_rule = (
        # read ios from user agent
        df['user_agent'].str.contains("ios", na=False, case = False) |
        df['user_agent'].str.contains("captivenetworksupport", na=False, case = False) |
        df['user_agent'].str.contains("iphone.OS", regex = True, na=False, case = False) |
        # infer from model
        df['model'].str.contains('iphone', na=False, case=False)
        #dhcp option 55 / parameter
    )

    df.loc[ios_rule, 'os'] = 'iOS'

    #option 55
    df.loc[df['params'].isin(params_ios), 'os'] = 'iOS'

    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df


def mark_os_mac(write_to_file=True):
    df = helper.get_df(config._didbName_)
    # macos_rule = (df['brand'] == 'Apple') & ((df['model'].str.contains('mac', na=False, case=False)))
    macos_rule = (
        df['model'].str.contains('mac', na=False, case=False) |
        df['model'].str.contains('Darwin/22.2.0', na=False, case = False)
    )
    df.loc[macos_rule, 'os'] = 'macOS'
    #option 55
    df.loc[df['params'].isin(params_macos), 'os'] = 'macOS'
    
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df


def mark_os_windows(write_to_file=True):
    df = helper.get_df(config._didbName_)
    windows_rule = (df['user_agent'].str.contains('microsoft-wns', na=False, case=False)) | (df['user_agent'].str.contains('microsoft', na=False, case=False)) | (df['user_agent'].str.contains('Microsoft-CryptoAPI', na=False, case=False)) | (df['vendor'].str.contains('MSFT', na=False, case=False))
    df.loc[windows_rule, 'os'] = 'Windows'
    #option 55
    df.loc[df['params'].isin(params_windows), 'os'] = 'Windows' 
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_os_linux(write_to_file=True):
    df = helper.get_df(config._didbName_)
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
        df['user_agent'].str.contains('ubuntu', na=False, case=False) |
        df['user_agent'].str.contains('pacman', na=False, case=False)
    )
    linux_rule = linux_rule & (~df['user_agent'].str.contains('android', na=False, case=False))
    df.loc[linux_rule, 'os'] = 'Linux'
    #option 55
    df.loc[df['params'].isin(params_linux), 'os'] = 'Linux' 
    df.loc[df['params'].isin(params_linux_debian), 'os'] = 'Linux-debian' 

    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_os_android(write_to_file=True):
    df = helper.get_df(config._didbName_)
    #android_rule = (df['user_agent'].str.contains('android', na=False, case=False)) | (df['vendor'].str.contains('android', na=False, case=False))
    android_rule = (
        # read from hostname, user agent or vendor
        df['hostname'].str.contains('android', na=False, case=False) |
        df['vendor'].str.contains('android', na=False, case=False) |
        df['user_agent'].str.contains('android', na=False, case=False) |
        df['user_agent'].str.contains('dalvik',na=False,case=False)|
        # infer from model
        df['model'].str.contains('galaxy', na=False, case=False) 
        # type is mobile and brand is not apple
        # ((df['type'].str.contains('Mobile')) & (df['brand']!= 'Apple') & (df['brand']!=''))
    )
    df.loc[android_rule, 'os'] = 'Android'
    #option 55
    df.loc[df['params'].isin(params_android), 'os'] = 'Android' 
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df


def mark_os_nintendo3SDSS(write_to_file=True):
    df = helper.get_df(config._didbName_)
    
    nintendoOS_rule = (
        # infer from model
        df['model'].str.contains('nintendo 3ds', na=False, case=False)
    )
    
    df.loc[nintendoOS_rule, 'os'] = 'Nintendo 3DS System Software'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df


def mark_os_ipad(write_to_file=True):
    df = helper.get_df(config._didbName_)
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
    
    df.loc[df['params'].isin(params_ipad), 'os'] = 'iPadOS' 

    df.loc[ipadOS_rule, 'os'] = 'iPadOS'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

def mark_os_appleWatch(write_to_file=True):
    df = helper.get_df(config._didbName_)

    appleWatchOS_rule = df['model'].str.contains('appleWatch', na=False, case=False)
    
    df.loc[appleWatchOS_rule, 'os'] = 'watchOS'
    if write_to_file:
        helper.update_didb(df, config._didbName_)
    return df

 
def mark_os_unix(write_to_file=True):
    df = helper.get_df(config._didbName_)
    # android_rule = (df['user_agent'].str.contains('android', na=False, case=False)) | (df['vendor'].str.contains('android', na=False, case=False))
    
    unix_rule = (
        # read from user agent or vendor
        df['vendor'].str.contains('udhcp', na=False, case=False)
    )
    
    df.loc[unix_rule, 'os'] = 'UNIX'
    #option 55
    df.loc[df['params'].isin(params_unix), 'os'] = 'UNIX' 
    
    if write_to_file:
        helper.update_didb(df, config._didbName_)

def mark_missing_os_from_uaparser(write_to_file=True):
    df = helper.get_df(config._didbName_)

    no_os = df['os'].isna() & (df['ua_device_os'] != 'Other')

    df.loc[no_os, 'os'] = df.loc[no_os, 'ua_device_os']

    if write_to_file:
        helper.update_didb(df, config._didbName_)

    return df
