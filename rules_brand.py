import requests
import json
import pandas as pd
import pickle
import os
import helper


def mark_brand_apple(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    apple_rule = df['hostname'].str.contains('macbook', na=False, case=False) | df['hostname'].str.contains('iphone', na=False, case=False) | df['user_agent'].str.contains('iphone', na=False, case=False) | df['user_agent'].str.contains('macintosh', na=False, case=False) | df['hostname'].str.contains('MBP', na=False, case=True) | df['user_agent'].str.contains('CaptiveNetworkSupport', na=False, case=False) | df['user_agent'].str.contains('com.apple', na=False, case=False)
    
    df.loc[apple_rule, 'brand'] = 'Apple'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_brand_samsung(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    samsung_rule = df['hostname'].str.contains('samsung', na=False, case=False) | df['hostname'].str.contains('galaxy', na=False, case=False) | (df['user_agent'].str.contains('samsung', na=False, case=False) & ~df['user_agent'].str.contains('samsungbrowser', na=False, case=False))| df['user_agent'].str.contains('SM-', na=False, case=True)
    
    df.loc[samsung_rule, 'brand'] = 'Samsung'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_brand_hp(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    samsung_rule = df['hostname'].str.contains('hp', na=False, case=False) | df['vendor'].str.contains('hp', na=False, case=False)
    
    df.loc[samsung_rule, 'brand'] = 'HP'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_airties(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    samsung_rule = df['hostname'].str.contains('air4', na=False, case=False) | df['vendor'].str.contains('air4', na=False, case=False)
    
    df.loc[samsung_rule, 'brand'] = 'Airties'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_huawei(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    samsung_rule = df['hostname'].str.contains('huawei', na=False, case=False) | df['vendor'].str.contains('huawei', na=False, case=False)
    
    df.loc[samsung_rule, 'brand'] = 'Huawei'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_xiaomi(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    samsung_rule = df['hostname'].str.contains('xiaomi', na=False, case=False) | df['vendor'].str.contains('xiaomi', na=False, case=False)
    
    df.loc[samsung_rule, 'brand'] = 'Xiaomi'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_lenovo(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    samsung_rule = df['hostname'].str.contains('lenovo', na=False, case=False) | df['hostname'].str.contains('thinkpad', na=False, case=False) | df['vendor'].str.contains('lenovo', na=False, case=False) | df['vendor'].str.contains('thinkpad', na=False, case=False)
    
    df.loc[samsung_rule, 'brand'] = 'Lenovo'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_nintendo(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    nintendo_rule = df['user_agent'].str.contains('NX NIFM', na=False, case=False)
    df.loc[nintendo_rule, 'brand'] = 'Nintendo'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df
