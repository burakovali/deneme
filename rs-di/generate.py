import requests
import json
import pandas as pd
import pickle
import os
import helper, config
import assoc_parser, raw_user_agent_parse
from user_agents import parse
import fetcher

if not os.path.exists(config.didbFilePath):
    os.makedirs(config.didbFilePath)

def populate_didb(didbName, rule='ALL', write_to_csv=True):
    import rules
    print("Populating " + str(didbName) + ' ...')
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
    df_merged = merge_didb(didbName, False, True)
    if write_to_csv:
        didb_name_trailer = didbName.split('didb_')[1]
        processed_csv = os.path.join(config.didbFilePath, 'processed_didb_' + str(didb_name_trailer) + '.csv')
        merged_csv = os.path.join(config.didbFilePath, 'merged_didb_' + str(didb_name_trailer) + '.csv')
        helper.write_df_to_csv(df, processed_csv)
        helper.write_df_to_csv(df_merged, merged_csv)
    return df, df_merged

def create_didb(didbName='didb', files_to_use = {'user_agent': 'user_agent.json', 'dhcp_proc': 'dhcp_proc.json', 'assoc_req': 'assoc_req.json', 'raw_user_agent': 'raw_user_agent.json'}, write_to_file=True):

    user_agent_path = os.path.join(config.logFilePath, files_to_use['user_agent'])
    f_ua = open(user_agent_path)
    print("Loading " + str(files_to_use['user_agent']) + ' ...')
    data_ua = json.load(f_ua)

    dhcp_proc_path = os.path.join(config.logFilePath, files_to_use['dhcp_proc'])
    f_dhcp_proc = open(dhcp_proc_path)
    print("Loading " + str(files_to_use['dhcp_proc']) + ' ...')
    data_dhcp_proc = json.load(f_dhcp_proc)

    assoc_req_path = os.path.join(config.logFilePath, files_to_use['assoc_req'])
    f_assoc_req = open(assoc_req_path)
    print("Loading " + str(files_to_use['assoc_req']) + ' ...')
    data_assoc_req =  assoc_parser.parse_assoc_df(json.load(f_assoc_req))

    raw_user_agent_path = os.path.join(config.logFilePath, files_to_use['raw_user_agent'])
    f_rua = open(raw_user_agent_path)
    print("Loading " + str(files_to_use['raw_user_agent']) + ' ...')
    data_rua = raw_user_agent_parse.parse_user_agent(json.load(f_rua))

    didb_name_trailer = files_to_use['user_agent'].split('user_agent')[1].split('.')[0]
    print("Creating didb... " + str(didb_name_trailer))

    df_devices = pd.DataFrame(columns=['mac', 'gw_mac', 'user_agent', 'timestamp', 'hostname', 'params', 'vendor','assoc_req_spatial_stream','assoc_req_vendors','wfa_device_name',"ua_device_family","ua_device_brand","ua_device_os", 'isWiFi'])
    macs = []
    user_agents = []
    gw_macs = []
    hostnames = []
    ua_device_family=[]
    ua_device_brand=[]
    ua_device_os=[]
    assoc_reqs = []
    print("Running user_agent...")
    for item in data_ua:
        user_agent_temp= parse(item['user_agent'])
        row = {'mac': item['mac'], 'user_agent': item['user_agent'], 'hostname': None, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'assoc_req_spatial_stream': None, 'assoc_req_vendors':None,'wfa_device_name':None, 'ua_device_family':user_agent_temp.device.family, 'ua_device_brand':user_agent_temp.device.brand, 'ua_device_os':str(user_agent_temp.os.family), 'isWiFi': False}
        isThisDevice = (df_devices['mac'] == item['mac']) & (df_devices['gw_mac'] == item['gw_mac']) & (df_devices["user_agent"] == item['user_agent'])
        if df_devices[isThisDevice].empty: 
            df_devices = pd.concat([df_devices, pd.DataFrame(row, index=[0])], ignore_index=True)
            macs.append(item['mac'])
            user_agents.append(item['user_agent'])
            gw_macs.append(item['gw_mac'])
            ua_device_family.append(user_agent_temp.device.family)
            ua_device_brand.append(user_agent_temp.device.brand)
            ua_device_os.append(str(user_agent_temp.os.family))
        else:
            df_devices.loc[isThisDevice, 'timestamp'] = item['timestamp']
            df_devices.loc[isThisDevice, 'isWiFi'] = False
        # print(item['mac'])
        # print(item['user_agent'])
    print("Running Raw user_agent...")
    for item in data_rua:
        row = {'mac': item['mac'], 'user_agent': item['user_agent'], 'hostname': None, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'assoc_req_spatial_stream': None, 'assoc_req_vendors':None, 'wfa_device_name':None, 'ua_device_family':user_agent_temp.device.family, 'ua_device_brand':user_agent_temp.device.brand, 'ua_device_os':str(user_agent_temp.os.family), 'isWiFi': False}
        isThisDevice = (df_devices['mac'] == item['mac']) & (df_devices['gw_mac'] == item['gw_mac']) & (df_devices["user_agent"] == item['user_agent'])
        if df_devices[isThisDevice].empty:
            df_devices = pd.concat([df_devices, pd.DataFrame(row, index=[0])], ignore_index=True)
            macs.append(item['mac'])
            user_agents.append(item['user_agent'])
            gw_macs.append(item['gw_mac'])
            ua_device_family.append(user_agent_temp.device.family)
            ua_device_brand.append(user_agent_temp.device.brand)
            ua_device_os.append(str(user_agent_temp.os.family))
        else:
            df_devices.loc[isThisDevice, 'timestamp'] = item['timestamp']
            df_devices.loc[isThisDevice, 'isWiFi'] = False

    print("Running dhcp_proc...")
    for item in data_dhcp_proc:
        if (item['hostname'] != ""):
            thisHostname = str(item['hostname'])
        else:
            thisHostname = None
        if (item['vendor_id'] != "null"):
            thisVendor = str(item['vendor_id'])
        else:
            thisVendor = None
        if (item['parameters'] != ""):
            thisParams = str(item['parameters'])
            thisParams = thisParams.replace(',','-')
        else:
            thisParams = None
        row = {'mac': item['mac'], 'user_agent': None, 'hostname': thisHostname, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': thisParams, 'vendor': thisVendor, 'assoc_req_spatial_stream': None, 'assoc_req_vendors':None, 'wfa_device_name':None, 'isWiFi': False}
        isThisDevice = (df_devices['mac'] == item['mac']) & (df_devices['gw_mac'] == item['gw_mac']) & (df_devices["hostname"] == thisHostname)
        # if not df_devices[isThisDevice].empty:
        #     if thisHostname is not None:
        #         hostname_idx = list(df_devices.loc[isThisDevice, 'hostname'].index)
        #         for idx in hostname_idx:
        #             if (df_devices.loc[idx, 'hostname'] != None):
        #                 hostname = df_devices.loc[idx, 'hostname']
        #                 if (thisHostname not in hostname):
        #                     df_devices.loc[idx, 'hostname'] = df_devices.loc[idx, 'hostname'] + ',' + thisHostname
        #                     df_devices.loc[idx, 'timestamp'] = df_devices.loc[idx, 'timestamp'] + ',' + item['timestamp']
        #                     df_devices.loc[idx, 'isWiFi'] = False
        if df_devices[isThisDevice].empty:
            df_devices = pd.concat([df_devices, pd.DataFrame(row, index=[0])], ignore_index=True)
        else:
            df_devices.loc[isThisDevice, 'timestamp'] = item['timestamp']
        hostnames.append(thisHostname)
    
    print("Running assoc_req...")
    for item in data_assoc_req:
        if helper.check_if_valid_mac(item['device_mac']):
            device_mac = helper.unColonizeMAC(item['device_mac'])
        else:
            device_mac = None
        row = {'mac': device_mac, 'user_agent': None, 'hostname': None, 'gw_mac': item['gw_mac'], 'timestamp': item['timestamp'], 'params': None, 'vendor': None,'assoc_req_spatial_stream': item['spatial_stream'], 'assoc_req_vendors': item['vendors'],'wfa_device_name':item['wfa_device_name'], 'isWiFi': True}
        if not df_devices[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac'])].empty:
            # if not ('does not exist' in str(item['data'])):
            # df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), ['assoc_req_vendors','assoc_req_spatial_stream']] = [item['vendors'], item['spatial_stream']]
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'assoc_req_spatial_stream'] = item['spatial_stream']
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'assoc_req_vendors'] = item['vendors']
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'wfa_device_name'] = item['wfa_device_name']
            df_devices.loc[(df_devices['mac'] == device_mac) & (df_devices['gw_mac'] == item['gw_mac']), 'isWiFi'] = True
        else:
            if not (device_mac == None):
                df_devices = pd.concat([df_devices, pd.DataFrame(row, index=[0])], ignore_index=True)

    didbFileName = None
    if write_to_file:
        if didb_name_trailer != '':
            didbFileName = didbName + didb_name_trailer
        didbFile = os.path.join(config.didbFilePath, didbFileName)
        config.set_didbName(didbFileName)
        helper.write_pickle(df_devices, didbFile)

    return df_devices, didbFileName


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


def merge_didb(didbName='didb', create_combined_didb=False, write_to_file=True):

    if create_combined_didb:
        df = helper.get_merged_df(didbName)
    else:
        df = helper.get_df(didbName)

    macList = list(df['mac'].unique())

    merged_df = pd.DataFrame(columns=['mac', 'gw_mac', 'brand', 'model', 'modelVersion', 'os', 'osVersion', 'deviceType', 'isWiFi', 'isRandom', 'timestamp', 'hostname', 'params'])

    for mac in macList:
        # print(mac)
        if not helper.check_if_valid_mac(mac):
            # print("Not valid mac!")
            continue
        isRandom = helper.is_random(mac)
        sta_mac = helper.colonizeMAC(mac)
        gw_mac = list(df[df['mac'] == mac]['gw_mac'].unique())
        gw_mac = [x for x in gw_mac if str(x) != 'nan']
        gw_mac = ', '.join(gw_mac)
        if len(gw_mac) == 0:
            gw_mac = ''

        try:
            brand = list(df[df['mac'] == mac]['brand'].unique())
        except:
            brand = None
        if brand is not None:
            brand = [x for x in brand if str(x) != 'nan']
            brand = ', '.join(brand)
            if len(brand) == 0:
                brand = ''
        
        try:
            model = list(df[df['mac'] == mac]['model'].unique())
        except:
            model = None
        if model is not None:
            model = [x for x in model if str(x) != 'nan']
            model = [x for x in model if x is not None]
            model = ', '.join(model)
            if len(model) == 0:
                model = ''

        try:
            modelVersion = list(df[df['mac'] == mac]['modelVersion'].unique())
        except:
            modelVersion = None
        if modelVersion is not None:
            modelVersion = [x for x in modelVersion if str(x) != 'nan']
            modelVersion = ', '.join(modelVersion)
            if len(modelVersion) == 0:
                modelVersion = ''

        try:
            oss = list(df[df['mac'] == mac]['os'].unique())
        except:
            oss = None
        if oss is not None:
            oss = [x for x in oss if str(x) != 'nan']
            oss = ', '.join(oss)
            if len(oss) == 0:
                oss = ''

        try:
            osVersion = list(df[df['mac'] == mac]['osVersion'].unique())
        except:
            osVersion = None
        if osVersion is not None:
            osVersion = [x for x in osVersion if str(x) != 'nan']
            osVersion = ', '.join(osVersion)
            if len(osVersion) == 0:
                osVersion = ''

        try:
            deviceType = list(df[df['mac'] == mac]['deviceType'].unique())
        except:
            deviceType = None
        if deviceType is not None:
            deviceType = [x for x in deviceType if str(x) != 'nan']
            deviceType = ', '.join(deviceType)
            if len(deviceType) == 0:
                deviceType = ''

        try:
            params = list(df[df['mac'] == mac]['params'].unique())
        except:
            params = None
        if params is not None:
            params = [x for x in params if str(x) != 'nan' and x is not None]
            if len(params) == 0:
                params = ''
            else:
                params = ', '.join(params)

        try:
            iswifi = list(df[df['mac'] == mac]['isWiFi'].unique())
        except:
            iswifi = None
        if iswifi is not None:
            iswifi = [x for x in iswifi if str(x) != 'nan']
            if len(iswifi) == 0:
                iswifi = ''
            else:
                iswifi = any(iswifi)

        try:
            timestamp = list(df[df['mac'] == mac]['timestamp'].unique())
        except:
            timestamp = None
        if timestamp is not None:
            timestamp = [x for x in timestamp if str(x) != 'nan']
            if len(timestamp) == 0:
                latest_timestamp = ''
            else:
                latest_timestamp = max(timestamp)
                # timestamp = ', '.join(timestamp)

        try:
            hostName = list(df[df['mac'] == mac]['hostname'].unique())
        except:
            hostName = None
        if hostName is not None:
            hostName = [x for x in hostName if str(x) != 'nan' and x is not None]
            if len(hostName) == 0:
                hostName = ''
            else:
                hostName = ', '.join(hostName)

        row = {'mac': sta_mac, 'gw_mac': gw_mac, 'brand': brand, 'model': model, 'modelVersion': modelVersion, 'os': oss, 'osVersion': osVersion, 'deviceType': deviceType, 'timestamp': latest_timestamp, 'params': params, 'isWiFi': iswifi, 'isRandom': isRandom, 'hostname': hostName}

        merged_df = pd.concat([merged_df, pd.DataFrame(row, index=[0])], ignore_index=True)

        if write_to_file:
            if create_combined_didb:
                didbFile = os.path.join(config.didbFilePath, 'combined_didb')
                helper.write_pickle(merged_df, didbFile)
            else:
                didb_name_trailer = didbName.split('didb_')[1]
                didbFile = os.path.join(config.didbFilePath, 'merged_didb_' + str(didb_name_trailer))
                helper.write_pickle(merged_df, didbFile)
    return merged_df

def combine_didb(didbList, write_to_file=True):

    for di,dv in enumerate(didbList):
        print(str(dv))
        if di == 0:
            combined_df = helper.get_merged_df(dv)
        else:
            combined_df = pd.concat([combined_df, helper.get_merged_df(dv)], ignore_index=True)

    didbFile = os.path.join(config.didbFilePath, 'combined_didb')
    helper.write_pickle(combined_df, didbFile)
    merged_combined_df = merge_didb('combined_didb', True, True)

    if write_to_file:
        combined_csv = os.path.join(config.didbFilePath, 'combined_didb.csv')
        helper.write_df_to_csv(merged_combined_df, combined_csv)

    return combined_df


def create_and_populate_didb(didbName='didb', files_to_use = {'user_agent': 'user_agent.json', 'dhcp_proc': 'dhcp_proc.json', 'assoc_req': 'assoc_req.json', 'raw_user_agent': 'raw_user_agent.json'}, write_to_file=True):

    df, thisdidb = create_didb(didbName, files_to_use, True)
    populate_didb(thisdidb, 'ALL', True)


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
