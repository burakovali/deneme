import requests
import json
import pandas as pd
import pickle
import os
import httpagentparser
import re

    
def is_global(mac):
    if mac[1] == str(2) or mac[1] == str(6) or mac[1] == "a" or mac[1] == "e":
        # "Locally administered"
        return False
    else:
        # "Globally unique"
        return True
    
def hex_to_string(hex):
    if hex[:2] == '0x':
        hex = hex[2:]
    string_value = bytes.fromhex(hex).decode('utf-8')
    return string_value

def check_if_valid_mac(mac):
    if mac is not None:
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac.lower()):
            return True
    return False

def parse_useragent(str):
    data = httpagentparser.detect(str)
    platformName = None
    platformVersion = None
    os = None
    distName = None
    distVersion = None
    browserName = None
    browserVersion = None
    bot = None
    if "platform" in data:
        platformName = data['platform']['name']
        if "version" in data['platform']:
            platformVersion = data['platform']['version']
    if "os" in data:
        os = data['os']['name']
    if "dist" in data:
        distName = data['dist']['name']
        if "version" in data['dist']:
            distVersion = data['dist']['version']
    if "browser" in data:
        browserName = data['browser']['name']
        if "version" in data['browser']:
            browserVersion = data['browser']['version']
    if "bot" in data:
        bot = data['bot']
    
    parsed = {"platformName": platformName, "platformVersion": platformVersion, "os": os, "distName": distName, "distVersion": distVersion, "browserName": browserName, "browserVersion": browserVersion}
    return parsed

def write_pickle(data, fileName):
    # print("Writing to pickle!!")
    if fileName.rfind('/')!=-1:
        folderPath = fileName[:fileName.rfind('/')]
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
    filePath = os.path.join(fileName)
    with open(filePath, 'wb') as thefile:
        pickle.dump(data, thefile, protocol=-1)

def read_pickle(fileName):
    # print("Reading from pickle!!")
    filePath = os.path.join(fileName)
    data = []
    if os.path.exists(filePath):
        with open(filePath, 'rb') as thefile:
            data = pickle.load(thefile)
    return data

def get_df(didbName):
    didb_processed = str(didbName) + '_processed'
    if os.path.exists(didb_processed):
        df = read_pickle(didb_processed)
    else:
        df = read_pickle(didbName)
    return df

def get_merged_df(didbName):
    didb_processed = str(didbName) + '_merged'
    if os.path.exists(didb_processed):
        df = read_pickle(didb_processed)
    else:
        df = read_pickle(didbName)
    return df

def update_didb(df, didbName):
    didb_processed = str(didbName) + '_processed'
    write_pickle(df, didb_processed)
    return df

def delete_didb(didbName):
    didb_processed = str(didbName) + '_processed'
    if os.path.exists(didb_processed):
        print("Deleting previous processed didb...")
        os.remove(didb_processed)

def write_df_to_csv(df, filename):
    out = df.to_csv(filename, index=False)
    return out

def unColonizeMAC(mac):
    if not (mac == None):
        themac =  str(mac.replace(":",''))
    else:
        themac = None
    return themac

def colonizeMAC(mac):
    if len(mac.split(':')) == 1:
        themac = ''
        for mi, mv in enumerate(mac):
            themac = themac + mv
            if (mi+1)%2 == 0 and mi < 11:
                themac = themac + ':'
        return themac.lower()
    else:
        return mac

def check_oui(brandName, didbName='didb'):
    df_oui = read_pickle('ouiList')
    df = read_pickle(didbName)
    df['mac_oui'] = df['mac'].apply(lambda x: x[:6] if is_global(x[:6]) else None)
    mask = df['mac_oui'].notnull()
    df.loc[~mask, 'mac_oui'] = ''
    mask = df_oui['Assignment'].isin(df['mac_oui'])
    mask &= df_oui['Organization Name'].str.contains(brandName, case=False, na=False)
    matching_rows = df_oui.loc[mask]
    oui_rule = df['mac_oui'].isin(matching_rows['Assignment'])
    df.drop('mac_oui', axis=1, inplace=True)

    return oui_rule