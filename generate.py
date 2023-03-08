import requests
import json
import pandas as pd
import pickle
import os
import rules
import helper
import assoc_parser

def populate_didb(didbName, rule='ALL'):

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
    data_assoc_req =  assoc_parser.parse_assoc_df(json.load(f_assoc_req))

    print("Creating didb...")

    df_devices = pd.DataFrame(columns=['mac', 'gw_mac', 'user_agent', 'timestamp', 'hostname', 'params', 'vendor','assoc_req_spatial_stream','assoc_req_vendors',])
    macs = []
    user_agents = []
    gw_macs = []
    hostnames = []
    assoc_reqs = []
    for item in data_ua:
        row = {'mac': item['mac'], 'user_agent': item['user_agent'], 'hostname': None,'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'],'assoc_req_spatial_stream': None,'assoc_req_vendors':None }
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
        row = {'mac': item['mac'], 'user_agent': None, 'hostname': thisHostname, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': item['parameters'], 'vendor': thisVendor,'assoc_req_spatial_stream': None,'assoc_req_vendors':None }
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
        row = {'mac': device_mac, 'user_agent': None, 'hostname': None, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': None, 'vendor': None,'assoc_req_spatial_stream': item['spatial_stream'], 'assoc_req_vendors': item['vendors']}
        if not df_devices[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac'])].empty:
            # if not ('does not exist' in str(item['data'])):
            # df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), ['assoc_req_vendors','assoc_req_spatial_stream']] = [item['vendors'], item['spatial_stream']]
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'assoc_req_spatial_stream'] = item['spatial_stream']
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'assoc_req_vendors'] = item['vendors']
        else:
            if not (device_mac == None):
                    df_devices = df_devices.append(row, ignore_index=True)

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

    df_devices = pd.DataFrame(columns=['mac', 'gw_mac', 'user_agent', 'timestamp', 'hostname', 'assoc_req', 'op55Params'])

    macs = []
    user_agents = []
    gw_macs = []
    hostnames = []
    assoc_reqs = []
    for item in data_ua:
        row = {'mac': item['mac'], 'user_agent': item['user_agent'], 'hostname': None, 'assoc_req': None, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': item['parameters']}
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

    merged_df = pd.DataFrame(columns=['mac', 'gw_mac', 'brand', 'model', 'modelVersion', 'os', 'osVersion', 'deviceType', 'params'])

    for mac in macList:
        sta_mac = helper.colonizeMAC(mac)
        gw_mac = list(df[df['mac'] == mac]['gw_mac'].unique())
        gw_mac = [x for x in gw_mac if str(x) != 'nan']
        if len(gw_mac) == 0:
            gw_mac = ''
        try:
            brand = list(df[df['mac'] == mac]['brand'].unique())
        except:
            brand = None
        if brand is not None:
            brand = [x for x in brand if str(x) != 'nan']
            if len(brand) == 0:
                brand = ''

        try:
            model = list(df[df['mac'] == mac]['model'].unique())
        except:
            model = None
        if model is not None:
            model = [x for x in model if str(x) != 'nan']
            if len(model) == 0:
                model = ''

        try:
            modelVersion = list(df[df['mac'] == mac]['modelVersion'].unique())
        except:
            modelVersion = None
        if modelVersion is not None:
            modelVersion = [x for x in modelVersion if str(x) != 'nan']
            if len(modelVersion) == 0:
                modelVersion = ''

        try:
            os = list(df[df['mac'] == mac]['os'].unique())
        except:
            os = None
        if os is not None:
            os = [x for x in os if str(x) != 'nan']
            if len(os) == 0:
                os = ''

        try:
            osVersion = list(df[df['mac'] == mac]['osVersion'].unique())
        except:
            osVersion = None
        if osVersion is not None:
            osVersion = [x for x in osVersion if str(x) != 'nan']
            if len(osVersion) == 0:
                osVersion = ''

        try:
            deviceType = list(df[df['mac'] == mac]['deviceType'].unique())
        except:
            deviceType = None
        if deviceType is not None:
            deviceType = [x for x in deviceType if str(x) != 'nan']
            if len(deviceType) == 0:
                deviceType = ''

        try:
            params = list(df[df['mac'] == mac]['params'].unique())
        except:
            params = None
        if params is not None:
            params = [x for x in params if str(x) != 'nan']
            if len(params) == 0:
                params = ''

        row = {'mac': sta_mac, 'gw_mac': gw_mac, 'brand': brand, 'model': model, 'modelVersion': modelVersion, 'os': os, 'osVersion': osVersion, 'deviceType': deviceType, 'params': params}

        merged_df = merged_df.append(row, ignore_index=True)

        if write_to_file:
            helper.write_pickle(merged_df, 'didb_merged')
    return merged_df

def remove_nan (myList):
    if myList is not None:
        myList = [x for x in myList if str(x) != 'nan']
        if len(myList) == 0:
            myList = ''
    return myList    

def os_params_list(didbName='didb', write_to_file=True):

    df = helper.get_df(didbName)

    paramsList = list(df['params'].unique())

    osParam_df = pd.DataFrame(columns=['params', 'os', 'brands', 'models', 'modelVersions'])

    for myP in paramsList:
        try:
            myOS = list(df[df['params'] == myP]['os'].unique())
        except:
            myOS = None
        myOS = remove_nan(myOS)
        try:
            brands = list(df[df['params'] == myP]['brand'].unique())
        except:
            brands = None
        brands = remove_nan(brands)
        try:
            models = list(df[df['params'] == myP]['model'].unique())
        except:
            models = None
        models = remove_nan(models)
        try:
            modelVersions = list(df[df['params'] == myP]['modelVersion'].unique())
        except:
            modelVersions = None
        modelVersions = remove_nan(modelVersions) 

        row = {'params': myP, 'os': myOS, 'brands': brands, 'models': models, 'modelVersions': modelVersions}

        osParam_df = osParam_df.append(row, ignore_index=True)

        if write_to_file:
            helper.write_pickle(osParam_df, 'os_param_list')
    return osParam_df
