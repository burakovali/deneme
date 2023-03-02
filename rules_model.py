import requests
import json
import pandas as pd
import pickle
import os
import helper



def mark_model_iphone(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    iphone_rule = (df['brand'] == 'Apple') & ((df['hostname'].str.contains('iphone', na=False, case=False)) | (df['user_agent'].str.contains('iphone', na=False, case=False)))
    
    df.loc[iphone_rule, 'model'] = 'iphone'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_macBook(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    macBook_rule = ((df['brand'] == 'Apple') & ((df['hostname'].str.contains('macBook', na=False, case=False)) | (df['user_agent'].str.contains('macbook', na=False, case=False)) | (df['hostname'].str.contains('MBP', na=False, case=True))))
    
    df.loc[macBook_rule, 'model'] = 'macBook'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_macBookPro(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    macBookPro_rule = ((df['brand'] == 'Apple') & (df['model'] == 'macBook')) & ((df['hostname'].str.contains('pro', na=False, case=False)) | (df['user_agent'].str.contains('pro', na=False, case=False)) | (df['hostname'].str.contains('MBP', na=False, case=True)))
    
    df.loc[macBookPro_rule, 'model'] = 'macBookPro'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_galaxy(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    galaxy_rule = (df['brand'] == 'Samsung') & ((df['hostname'].str.contains('galaxy', na=False, case=False)) | (df['user_agent'].str.contains('galaxy', na=False, case=False)))
    galaxy_rule = (df['user_agent'].str.contains('SM-A115F', na=False, case=True)) | galaxy_rule

    df.loc[galaxy_rule, 'model'] = 'Galaxy'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_model_galaxyTab(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    galaxy_rule = (df['brand'] == 'Samsung') & ((df['hostname'].str.contains('galaxy', na=False, case=False)) | (df['user_agent'].str.contains('galaxy', na=False, case=False)))
    galaxyTab_rule = (galaxy_rule) & (df['model'] == 'Galaxy') & ((df['hostname'].str.contains('tab', na=False, case=False)) | (df['user_agent'].str.contains('tab', na=False, case=False)))
    galaxyTab_rule = (df['user_agent'].str.contains('SM-P610', na=False, case=True)) | galaxyTab_rule
    
    df.loc[galaxyTab_rule, 'model'] = 'GalaxyTab'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df
    
def mark_model_hpPrinter(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    hpPrinter_rule = (df['brand'] == 'HP') & ((df['vendor'].str.contains('print', na=False, case=False)) | (df['vendor'].str.contains('laserj', na=False, case=False)))
    
    df.loc[hpPrinter_rule, 'model'] = 'Printer'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_model_thinkpad(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)

    galaxyTab_rule = (df['brand'] == 'Lenovo') & ((df['vendor'].str.contains('thinkpad', na=False, case=False)) | (df['hostname'].str.contains('thinkpad', na=False, case=False)))
    
    df.loc[galaxyTab_rule, 'model'] = 'ThinkPad'
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