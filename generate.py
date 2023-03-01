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
        device_mac = helper.unColonizeMAC(item['device_mac'])
        row = {'mac': device_mac, 'user_agent': None, 'hostname': None, 'assoc_req': item['data'], 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': None, 'vendor': None}
        if not df_devices[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac'])].empty:
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'assoc_req'] = item['data']
        else:
            if not (device_mac == None):
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
