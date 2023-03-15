import requests
import json
import pandas as pd
import pickle
import os
import helper

params_iphone = ['1,121,3,6,15,108,114,119,252']
params_macbook = ['1,121,3,6,15,114,119,252,95,44,46']
params_macbookPro = ['1,121,3,6,15,108,114,119,252,95,44,46', '1,121,3,6,15,119,252,95,44,46']
params_printer = ['1,121,33,3,6,12,15,28,44,51,54,58,59,81,119,252', '6,3,1,15,12,44,81,69,42,43,18,66,67,150,7']
params_ps5 = ['1,3,15,6']

def mark_model_iphone(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    # iphone_rule = (df['brand'] == 'Apple') & ((df['hostname'].str.contains('iphone', na=False, case=False)) | (df['user_agent'].str.contains('iphone', na=False, case=False)))
    
    iphone_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('iphone', na=False, case=False) |
        df['user_agent'].str.contains('iphone', na=False, case=False) |
        df['vendor'].str.contains('iphone', na=False, case=False)
        # apple and phone
        # ((df['brand'] == "Apple") & (df['type'] == 'Mobile'))
    )

    df.loc[iphone_rule, 'model'] = 'iPhone'
    #option 55
    df.loc[df['params'].isin(params_iphone), 'model'] = 'iPhone'

    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_ipad(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    #iphone_rule = (df['brand'] == 'Apple') & ((df['hostname'].str.contains('iphone', na=False, case=False)) | (df['user_agent'].str.contains('iphone', na=False, case=False)))
    ipad_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('ipad', na=False, case=False) |
        df['user_agent'].str.contains('ipad', na=False, case=False) |
        df['vendor'].str.contains('ipad', na=False, case=False)
    )
    
    df.loc[ipad_rule, 'model'] = 'iPad'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_ipadPro(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    #iphone_rule = (df['brand'] == 'Apple') & ((df['hostname'].str.contains('iphone', na=False, case=False)) | (df['user_agent'].str.contains('iphone', na=False, case=False)))
    ipadPro_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('ipad.pro', regex = True, na=False, case=False) |
        df['user_agent'].str.contains('ipad.pro', regex = True, na=False, case=False) |
        df['vendor'].str.contains('ipad.pro', regex = True, na=False, case=False)
    )
    
    df.loc[ipadPro_rule, 'model'] = 'iPadPro'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_macBook(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    # macBook_rule = ((df['brand'] == 'Apple') & ((df['hostname'].str.contains('macBook', na=False, case=False)) | (df['user_agent'].str.contains('macbook', na=False, case=False)) | (df['hostname'].str.contains('MBP', na=False, case=True))))
    
    macBook_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('macbook', na=False, case=False) |
        df['user_agent'].str.contains('macbook', na=False, case=False) |
        df['vendor'].str.contains('macbook', na=False, case=False)
    )

    df.loc[macBook_rule, 'model'] = 'macBook'
    #option 55
    df.loc[df['params'].isin(params_macbook), 'model'] = 'macBook'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_macBookPro(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    # macBookPro_rule = ((df['brand'] == 'Apple') & (df['model'] == 'macBook')) & ((df['hostname'].str.contains('pro', na=False, case=False)) | (df['user_agent'].str.contains('pro', na=False, case=False)) | (df['hostname'].str.contains('MBP', na=False, case=True)))
    
    macBookPro_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('macbook.pro', regex = True, na=False, case=False) |
        df['user_agent'].str.contains('macbook.pro', regex = True, na=False, case=False) |
        df['vendor'].str.contains('macbook.pro', regex = True, na=False, case=False) |
        df['hostname'].str.contains('MBP', na=False, case=True) |
        df['user_agent'].str.contains('MBP', na=False, case=True) |
        df['vendor'].str.contains('MBP', na=False, case=True) 
    )

    df.loc[macBookPro_rule, 'model'] = 'macBookPro'
    #option 55
    df.loc[df['params'].isin(params_macbookPro), 'model'] = 'macBookPro'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_appleWatch(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    appleWatch_rule = (
        # read from hostname, user agent, vendor
        df['assoc_req_vendors'].str.contains('apple', regex = True, na=False, case=False) &
        df['assoc_req_vendors'].str.contains('microsoft', regex = True, na=False, case=False) &
        ~df['assoc_req_vendors'].str.contains('epigram', regex = True, na=False, case=False) &
        (df['assoc_req_spatial_stream'] == 1)
    )

    df.loc[appleWatch_rule, 'model'] = 'appleWatch'

    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_galaxy(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # galaxy_rule =  (df['brand'] == 'Samsung') & ((df['hostname'].str.contains('galaxy', na=False, case=False)) | (df['user_agent'].str.contains('galaxy', na=False, case=False)))
    # galaxy_rule = (df['user_agent'].str.contains('SM-A115F', na=False, case=True)) | galaxy_rule

    galaxy_rule = (
        # read from hsotname, vendor or user agent
        df['hostname'].str.contains('galaxy', na=False, case=False) |
        df['user_agent'].str.contains('galaxy', na=False, case=False) |
        df['vendor'].str.contains('galaxy', na=False, case=False) |
        df['user_agent'].str.contains('SM-A115F', na=False, case=False) | 
        df['user_agent'].str.contains('SM-G965F', na=False, case=False) # TODO add all galaxy model numbers
    )

    df.loc[galaxy_rule, 'model'] = 'Galaxy'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_galaxyTab(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    # galaxy_rule = (df['brand'] == 'Samsung') & ((df['hostname'].str.contains('galaxy', na=False, case=False)) | (df['user_agent'].str.contains('galaxy', na=False, case=False)))
    # galaxyTab_rule = (galaxy_rule) & (df['model'] == 'Galaxy') & ((df['hostname'].str.contains('tab', na=False, case=False)) | (df['user_agent'].str.contains('tab', na=False, case=False)))
    # galaxyTab_rule = (df['user_agent'].str.contains('SM-P610', na=False, case=True)) | galaxyTab_rule
    
    galaxyTab_rule = (
        df['hostname'].str.contains('galaxy.tab', na=False, case=False) |
        df['user_agent'].str.contains('galaxy.tab', na=False, case=False) |
        df['vendor'].str.contains('galaxy.tab', na=False, case=False) |
        df['user_agent'].str.contains('SM-P610', na=False, case=False) # TODO add all galaxy tab model numbers
    )

    df.loc[galaxyTab_rule, 'model'] = 'GalaxyTab'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df
    
def mark_model_hpPrinter(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    # hpPrinter_rule = (df['brand'] == 'HP') & ((df['vendor'].str.contains('print', na=False, case=False)) | (df['vendor'].str.contains('laserj', na=False, case=False)))
    
    hpPrinter_rule = (
        # HP brand and printer
        # df['brand'] == 'HP') & ((df['vendor'].str.contains('print', na=False, case=False)) |
        # read from hostname, user agent or vendor
        (df['hostname'].str.contains('laserj', na=False, case=False)) |
        (df['user_agent'].str.contains('laserj', na=False, case=False)) |
        (df['vendor'].str.contains('HP laserj', na=False, case=False)) |
        (df['vendor'].str.contains('HP print', na=False, case=False))
    )

    df.loc[hpPrinter_rule, 'model'] = 'Printer'
    #option 55
    df.loc[df['params'].isin(params_printer), 'model'] = 'Printer'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_thinkpad(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    # galaxyTab_rule = (df['brand'] == 'Lenovo') & ((df['vendor'].str.contains('thinkpad', na=False, case=False)) | (df['hostname'].str.contains('thinkpad', na=False, case=False)))
    
    thinkpad_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('thinkpad', na=False, case=False)) | 
        (df['hostname'].str.contains('thinkpad', na=False, case=False)) |
        (df['user_agent'].str.contains('thinkpad', na=False, case=False))
    )

    df.loc[thinkpad_rule, 'model'] = 'ThinkPad'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_nintendo(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    nintendo_rule = df['user_agent'].str.contains('NX NIFM', na=False, case=False)
    df.loc[nintendo_rule, 'model'] = 'Nintendo 3DS'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_elitebook(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    elitebook_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('elitebook', na=False, case=False)) | 
        (df['hostname'].str.contains('elitebook', na=False, case=False)) |
        (df['user_agent'].str.contains('elitebook', na=False, case=False))
    )
    
    df.loc[elitebook_rule, 'model'] = 'EliteBook'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_huaweiP(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    huaweiP_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('huawei.p', regex = True, na=False, case=False)) | 
        (df['hostname'].str.contains('huawei.p', regex = True, na=False, case=False)) |
        (df['user_agent'].str.contains('huawei.p', regex = True, na=False, case=False))
    )
    
    df.loc[huaweiP_rule, 'model'] = 'Huawei-P'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_xiaomiMi(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    xiaomiMi_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('xiaomi.mi', regex = True, na=False, case=False)) | 
        (df['hostname'].str.contains('xiaomi.mi', regex = True, na=False, case=False)) |
        (df['user_agent'].str.contains('xiaomi.mi', regex = True, na=False, case=False)) |
        (df['user_agent'].str.contains('MI 8', na=False, case=False)) |
        (df['vendor'].str.contains('MI8', na=False, case=True)) | 
        (df['hostname'].str.contains('MI8', na=False, case=True)) |
        (df['user_agent'].str.contains('MI8', na=False, case=True))
    )
    
    df.loc[xiaomiMi_rule, 'model'] = 'Xiaomi-Mi'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_mediapad(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    mediaPad_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('mediapad', na=False, case=False)) | 
        (df['hostname'].str.contains('mediapad', na=False, case=False)) |
        (df['user_agent'].str.contains('mediapad', na=False, case=False))
    )
    
    df.loc[mediaPad_rule, 'model'] = 'MediaPad'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_playStation(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    playStation_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('PS5', na=False, case=False)) | 
        (df['hostname'].str.contains('PS5', na=False, case=False)) |
        (df['user_agent'].str.contains('PS5', na=False, case=False))
    )
    
    df.loc[playStation_rule, 'model'] = 'PlayStation'
    #option 55
    df.loc[df['params'].isin(params_ps5), 'model'] = 'PlayStation'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_air4960(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    air4960_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('Air496', na=False, case=False)) | 
        (df['hostname'].str.contains('Air4960', na=False, case=False)) |
        (df['user_agent'].str.contains('Air4960', na=False, case=False))
    )
    
    df.loc[air4960_rule, 'model'] = 'Air4960'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_air4443(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    air4443_rule = (
        # read from user agent, vendor or hostname
        (df['vendor'].str.contains('Air444', na=False, case=False)) | 
        (df['hostname'].str.contains('Air4443', na=False, case=False)) |
        (df['user_agent'].str.contains('Air444', na=False, case=False))
    )
    
    df.loc[air4443_rule, 'model'] = 'Air4443'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_oneday(didbName='didb', write_to_file=True): #xiaomi
    df = helper.get_df(didbName)

    ondeday_rule = (
        (df['user_agent'].str.contains('oneday', na=False, case=False))
    )
    
    df.loc[ondeday_rule, 'model'] = 'Oneday'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df
