import requests
import json
import pandas as pd
import pickle
import os
import helper
import rules


def mark_brand_apple(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # apple_rule = df['hostname'].str.contains('macbook', na=False, case=False) | df['hostname'].str.contains('iphone', na=False, case=False) | df['user_agent'].str.contains('iphone', na=False, case=False) | df['user_agent'].str.contains('macintosh', na=False, case=False) | df['hostname'].str.contains('MBP', na=False, case=True) | df['user_agent'].str.contains('CaptiveNetworkSupport', na=False, case=False) | df['user_agent'].str.contains('com.apple', na=False, case=False)
    
    apple_rule = (
        # read apple from hostname, user agent, vendor name
        df['hostname'].str.contains('apple', na= False, case=False) |
        #df['user_agent'].str.contains('apple', na= False, case=False) |
        df['vendor'].str.contains('apple', na= False, case=False) |
        # infer from model
        (df['model'] == "iPhone") | (df['model'] == "macBook") | (df['model'] == "macBookPro") | (df['model'] == "iPad") | (df['model'] == 'macintosh') |
        # infer from user agent
        df['user_agent'].str.contains('CaptiveNetworkSupport', na= False, case=False) |
        df['user_agent'].str.contains('com.apple', na= False, case=False) |
        # infer from OS
        (df['os'] == "iOS") | (df['os'] == "macOS") | (df['os'] == "iPadOS")
    )


    df.loc[apple_rule, 'brand'] = 'Apple'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_brand_samsung(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # samsung_rule = df['hostname'].str.contains('samsung', na=False, case=False) | df['hostname'].str.contains('galaxy', na=False, case=False) | (df['user_agent'].str.contains('samsung', na=False, case=False) & ~df['user_agent'].str.contains('samsungbrowser', na=False, case=False))| df['user_agent'].str.contains('SM-', na=False, case=True)
    
    samsung_rule = (
        # read samsung from hostname, user agent or vendor id
        df['hostname'].str.contains('samsung', na= False, case=False) |
        #df['user_agent'].str.contains('samsung', na= False, case=False) |
        df['vendor'].str.contains('samsung', na= False, case=False) |
        # infer from model
        (df['model'] == "Galaxy") | (df['model'] == "GalaxyTab")
    )

    df.loc[samsung_rule, 'brand'] = 'Samsung'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_brand_hp(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # samsung_rule = df['hostname'].str.contains('hp', na=False, case=False) | df['vendor'].str.contains('hp', na=False, case=False)
    
    hp_rule = (
        # read from hostname or vendor
        df['hostname'].str.contains('HP ', na=False, case=True) |
        df['hostname'].str.contains('HP-', na=False, case=True) |
        df['vendor'].str.contains('HP ', na=False, case=True) |
        df['vendor'].str.contains('HP-', na=False, case=True) |
        # infer from model
        df['model'].str.contains('laserje', na=False, case=False) |
        df['model'].str.contains('elitebook', na=False, case=False)
    )

    df.loc[hp_rule, 'brand'] = 'HP'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_airties(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # samsung_rule = df['hostname'].str.contains('air4', na=False, case=False) | df['vendor'].str.contains('air4', na=False, case=False)
    
    airties_rule = (
        # read from hostname or vendor
        df['hostname'].str.contains(pat = '(Air[0-9]{4,})', regex = True, na=False, case=False) |
        df['vendor'].str.contains(pat = '(Air[0-9]{4,})', regex = True, na=False, case=False) |
        # infer from model
        df['model'].str.contains(pat = '(Air[0-9]{4,})', regex = True, na=False, case=False)
    )

    df.loc[airties_rule, 'brand'] = 'Airties'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_huawei(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # samsung_rule = df['hostname'].str.contains('huawei', na=False, case=False) | df['vendor'].str.contains('huawei', na=False, case=False)
    
    huawei_rule = (
        # read from hostname, vendor or user agent
        df['hostname'].str.contains('huawei', na=False, case=False) |
        df['vendor'].str.contains('huawei', na=False, case=False) |
        #df['user_agent'].str.contains('huawei', na=False, case=False) |
        # infer from model, example: Huawei P Series
        df['model'].str.contains('huawei', na=False, case=False)
    )

    df.loc[huawei_rule, 'brand'] = 'Huawei'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_xiaomi(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # samsung_rule = df['hostname'].str.contains('xiaomi', na=False, case=False) | df['user_agent'].str.contains('xiaomi', na=False, case=False) |df['vendor'].str.contains('xiaomi', na=False, case=False)   
    
    xiaomi_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('xiaomi', na=False, case=False) |
        df['vendor'].str.contains('xiaomi', na=False, case=False)|
        df['user_agent'].str.contains('xiaomi', na=False, case=False) |
        # infer from model
        df['model'].str.contains('Xiaomi', na=False, case=False) |
        df['model'].str.contains('Mediapad', na=False, case=False)
    )

    df.loc[xiaomi_rule, 'brand'] = 'Xiaomi'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_lenovo(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # samsung_rule = df['hostname'].str.contains('lenovo', na=False, case=False) | df['hostname'].str.contains('thinkpad', na=False, case=False) | df['vendor'].str.contains('lenovo', na=False, case=False) | df['vendor'].str.contains('thinkpad', na=False, case=False)
    
    lenovo_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('lenovo', na=False, case=False) |
        df['vendor'].str.contains('lenovo', na=False, case=False)|
        #df['user_agent'].str.contains('lenovo', na=False, case=False) |
        # infer from model
        df['model'].str.contains('ThinkPad', na=False, case=False)
    )

    df.loc[lenovo_rule, 'brand'] = 'Lenovo'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_nintendo(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    # nintendo_rule = df['user_agent'].str.contains('NX NIFM', na=False, case=False)
    
    nintendo_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('nintendo', na=False, case=False) |
        df['vendor'].str.contains('nintendo', na=False, case=False)|
        df['user_agent'].str.contains('nintendo', na=False, case=False) |
        # infer from model
        df['model'].str.contains('nintendo', na=False, case=False) |
        df['user_agent'].str.contains('NX NIFM', na=False, case=False)
    )

    df.loc[nintendo_rule, 'brand'] = 'Nintendo'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df

def mark_brand_sony(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    
    sony_rule = (
        # read from hostname, user agent, vendor
        df['hostname'].str.contains('sony', na=False, case=False) |
        df['vendor'].str.contains('sony', na=False, case=False) |
        #df['user_agent'].str.contains('sony', na=False, case=False) |
        # infer from model
        df['model'].str.contains('PlayStation', na=False, case=False) |
        # infer from OS
        df['os'].str.contains('FreeBSD', na=False, case=False)
    )
    
    df.loc[sony_rule, 'brand'] = 'Lenovo'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df