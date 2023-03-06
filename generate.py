import requests
import json
import pandas as pd
import pickle
import os
import rules
import helper

def populate_didb(didbName, rule='BRAND'):

    helper.delete_didb(didbName) # Clear the previously stored processed_didb
    print("Running rules...")
    if rule == 'ALL':
        for rule in rules.all_rules:
            for ri,rv in enumerate(rule):
                print(rv)
                rv()
    elif rule == 'BRAND':
        for ri,rv in enumerate(rules.brand_rules):
            rv()
    elif rule == 'MODEL':
        for ri,rv in enumerate(rules.model_rules):
            rv()
    elif rule == 'MODELVERSION':
        for ri,rv in enumerate(rules.modelVersion_rules):
            rv()
    elif rule == 'OS':
        for ri,rv in enumerate(rules.os_rules):
            rv()
    elif rule == 'OSVERSION':
        for ri,rv in enumerate(rules.osVersion_rules):
            rv()
    elif rule == 'DEVICETYPE':
        for ri,rv in enumerate(rules.deviceType_rules):
            rv()
    else:
        print('RULE UNDEFINED!')
        exit()
            
    df = helper.get_df(didbName)
    return df

def create_didb(didbName='didb', write_to_file=True):

    f_ua = open('user_agent.json')
    data_ua = json.load(f_ua)
    f_dhcp_proc = open('dhcp_proc.json')
    data_dhcp_proc = json.load(f_dhcp_proc)
    f_assoc_req = open('assoc_req.json')
    data_assoc_req = json.load(f_assoc_req)

    print("Creating didb...")

    df_devices = pd.DataFrame(columns=['mac', 'gw_mac', 'user_agent', 'timestamp', 'hostname', 'assoc_req', 'params', 'vendor'])

    macs = []
    user_agents = []
    gw_macs = []
    hostnames = []
    assoc_reqs = []
    for item in data_ua:
        row = {'mac': item['mac'], 'user_agent': item['user_agent'], 'hostname': None, 'assoc_req': None, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': None, 'vendor': None}
        isThisDevice = (df_devices['mac'] == item['mac']) & (df_devices['gw_mac'] == item['gw_mac']) & (df_devices["user_agent"] == item['user_agent'])
        if df_devices[isThisDevice].empty: 
            df_devices = df_devices.append(row, ignore_index=True)
            macs.append(item['mac'])
            user_agents.append(item['user_agent'])
            gw_macs.append(item['gw_mac'])
        else:
            df_devices.loc[isThisDevice, 'timestamp'] = item['timestamp']
        # print(item['mac'])
        # print(item['user_agent'])

    for item in data_dhcp_proc:
        if (item['hostname'] != ""):
            thisHostname = str(item['hostname'])
        else:
            thisHostname = None
        if (item['vendor_id'] != "null"):
            thisVendor = str(item['vendor_id'])
        else:
            thisVendor = None
        row = {'mac': item['mac'], 'user_agent': None, 'hostname': thisHostname, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': item['parameters'], 'vendor': thisVendor}
        isThisDevice = (df_devices['mac'] == item['mac']) & (df_devices['gw_mac'] == item['gw_mac'])
        if not df_devices[isThisDevice].empty:
            if thisHostname is not None:
                hostname_idx = list(df_devices.loc[isThisDevice, 'hostname'].index)
                for idx in hostname_idx:
                    if (df_devices.loc[idx, 'hostname'] != None):
                        hostname = df_devices.loc[idx, 'hostname']
                        if (thisHostname not in hostname):
                            df_devices.loc[idx, 'hostname'] = df_devices.loc[idx, 'hostname'] + ',' + thisHostname
                            df_devices.loc[idx, 'timestamp'] = df_devices.loc[idx, 'timestamp'] + ',' + item['timestamp']
        
        else:
            df_devices = df_devices.append(row, ignore_index=True)
        hostnames.append(thisHostname)
  
    for item in data_assoc_req:
        if helper.check_if_valid_mac(item['device_mac']):
            device_mac = helper.unColonizeMAC(item['device_mac'])
        else:
            device_mac = None
        row = {'mac': device_mac, 'user_agent': None, 'hostname': None, 'assoc_req': item['data'], 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': None, 'vendor': None}
        if not df_devices[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac'])].empty:
            # if not ('does not exist' in str(item['data'])):
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'assoc_req'] = item['data']
        else:
            if not (device_mac == None):
                if not ('does not exist' in str(item['data'])):
                    # print(device_mac + ' does not exist...')
                    df_devices = df_devices.append(row, ignore_index=True)
        assoc_reqs.append(item['data'])

    if write_to_file:
        helper.write_pickle(df_devices, didbName)

    return df_devices


def create_didb_redundant(write_to_file=False):

    f_ua = open('user_agent.json')
    data_ua = json.load(f_ua)
    f_dhcp_proc = open('dhcp_proc.json')
    data_dhcp_proc = json.load(f_dhcp_proc)
    f_assoc_req = open('assoc_req.json')
    data_assoc_req = json.load(f_assoc_req)

    df_devices = pd.DataFrame(columns=['mac', 'gw_mac', 'user_agent', 'timestamp', 'hostname', 'assoc_req'])

    macs = []
    user_agents = []
    gw_macs = []
    hostnames = []
    assoc_reqs = []
    for item in data_ua:
        row = {'mac': item['mac'], 'user_agent': item['user_agent'], 'hostname': None, 'assoc_req': None, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp']}
        isThisDevice = (df_devices['mac'] == item['mac']) & (df_devices['gw_mac'] == item['gw_mac']) & (df_devices["user_agent"] == item['user_agent'])
        if df_devices[isThisDevice].empty: 
            df_devices = df_devices.append(row, ignore_index=True)
            macs.append(item['mac'])
            user_agents.append(item['user_agent'])
            gw_macs.append(item['gw_mac'])
        else:
            df_devices.loc[isThisDevice, 'timestamp'] = item['timestamp']

    for item in data_dhcp_proc:
        if (item['hostname'] != ""):
            thisHostname = str(item['hostname'])
        else:
            thisHostname = None
        row = {'mac': item['mac'], 'user_agent': None, 'hostname': thisHostname, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp']}
        isThisDevice = (df_devices['mac'] == item['mac']) & (df_devices['gw_mac'] == item['gw_mac']) & (df_devices["hostname"] == item['hostname'])
        if df_devices[isThisDevice].empty:
            df_devices = df_devices.append(row, ignore_index=True)
            macs.append(item['mac'])
            hostnames.append(thisHostname)
            gw_macs.append(item['gw_mac'])
        else:
            df_devices.loc[isThisDevice, 'timestamp'] = item['timestamp']
        
    for item in data_assoc_req:
        device_mac = helper.unColonizeMAC(item['device_mac'])
        row = {'mac': device_mac, 'user_agent': None, 'hostname': None, 'assoc_req': item['data'], 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp']}
        isThisDevice = (df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']) & (df_devices["assoc_req"] == item['data'])
        if df_devices[isThisDevice].empty: 
            df_devices = df_devices.append(row, ignore_index=True)
            macs.append(device_mac)
            assoc_reqs.append(item['data'])
            gw_macs.append(item['gw_mac'])
        else:
            df_devices.loc[isThisDevice, 'timestamp'] = item['timestamp']
    
    if write_to_file:
        helper.write_pickle(df_devices, 'didb_redundant')

    return df_devices


def merge_didb(didbName='didb', write_to_file=True):

    df = helper.get_df(didbName)

    macList = list(df['mac'].unique())

    merged_df = pd.DataFrame(columns=['mac', 'gw_mac', 'brand', 'model', 'modelVersion', 'os', 'osVersion', 'deviceType'])

    for mac in macList:
        sta_mac = helper.colonizeMAC(mac)
        gw_mac = list(df[df['mac'] == mac]['gw_mac'].unique())
        gw_mac = [x for x in gw_mac if str(x) != 'nan']
        if len(gw_mac) == 0:
            gw_mac = ''
        try:
            brand = list(df[df['mac'] == mac]['brand'].unique())
            brand = [x for x in brand if str(x) != 'nan']
            if len(brand) == 0:
                brand = ''
        except:
            brand = None

        try:
            model = list(df[df['mac'] == mac]['model'].unique())
            model = [x for x in model if str(x) != 'nan']
            if len(model) == 0:
                model = ''
        except:
            model = None

        try:
            modelVersion = list(df[df['mac'] == mac]['modelVersion'].unique())
            modelVersion = [x for x in modelVersion if str(x) != 'nan']
            if len(modelVersion) == 0:
                modelVersion = ''
        except:
            modelVersion = None

        try:
            os = list(df[df['mac'] == mac]['os'].unique())
            os = [x for x in os if str(x) != 'nan']
            if len(os) == 0:
                os = ''
        except:
            os = None

        try:
            osVersion = list(df[df['mac'] == mac]['osVersion'].unique())
            osVersion = [x for x in osVersion if str(x) != 'nan']
            if len(osVersion) == 0:
                osVersion = ''
        except:
            osVersion = None

        try:
            deviceType = list(df[df['mac'] == mac]['deviceType'].unique())
            deviceType = [x for x in deviceType if str(x) != 'nan']
            if len(deviceType) == 0:
                deviceType = ''
        except:
            deviceType = None

        row = {'mac': sta_mac, 'gw_mac': gw_mac, 'brand': brand, 'model': model, 'modelVersion': modelVersion, 'os': os, 'osVersion': osVersion, 'deviceType': deviceType}

        merged_df = merged_df.append(row, ignore_index=True)

        if write_to_file:
            helper.write_pickle(merged_df, 'didb_merged')
    return merged_df
