import requests
import json
import pandas as pd
import pickle
import os
import helper, config
from datetime import datetime, timedelta

# DHCP http://cloud-dpi.herokuapp.com/api/dhcp_processed_api/
# DHCP unprocessed http://cloud-dpi.herokuapp.com/api/dhcp_api/
# Token 71770dd90492c70863464e214113679b3d8bb5ae
# user agent http://cloud-dpi.herokuapp.com/api/identified_devices/
# assoc req http://cloud-dpi.herokuapp.com/api/assoc_req/
# curl --location --request GET 'http://cloud-dpi.herokuapp.com/api/dhcp_processed_api/' --header 'Authorization: Token 71770dd90492c70863464e214113679b3d8bb5ae'

if not os.path.exists(config.logFilePath):
    os.makedirs(config.logFilePath)

def get_data(dateInfo, type='ALL'):
    myheaders = {'Authorization': 'Token 71770dd90492c70863464e214113679b3d8bb5ae'}
    if type == 'ALL':
        print("Getting ALL data...")
        dhcp_proc = 'http://cloud-dpi.herokuapp.com/api/dhcp_processed_api/'
        dhcp = 'http://cloud-dpi.herokuapp.com/api/dhcp_api/'
        user_agent = 'http://cloud-dpi.herokuapp.com/api/identified_devices/'
        raw_user_agent = 'https://cloud-dpi.herokuapp.com/api/raw_user_agent/'
        assoc_req = 'http://cloud-dpi.herokuapp.com/api/assoc_req/'
        conntrack = 'https://cloud-dpi.herokuapp.com/api/conntrack_events'

    if dateInfo['use_timeRange']:
        endDate = dateInfo['endDate']
        if dateInfo['interval'] == None:
            startDate = dateInfo['startDate']
        else:
            interval = int(dateInfo['interval'])
            theEnd = datetime.strptime(dateInfo['endDate'], '%Y-%m-%d %H:%M:%S')
            startDate = theEnd - timedelta(hours = interval)
            startDate = startDate.strftime("%Y-%m-%d %H:%M:%S")
            if startDate < dateInfo['startDate']:
                startDate = dateInfo['startDate']

        payload = {'records_after': startDate, 'records_before': endDate}
        print("Using dates between " + startDate + ' and ' + endDate)

        myDate_after = startDate.replace(':','-')
        myDate_after = myDate_after.replace(' ','-')
        myDate_before = endDate.replace(':','-')
        myDate_before = myDate_before.replace(' ','-')

        fn_dhcp = os.path.join(config.logFilePath, 'dhcp_' + myDate_after + '_' + myDate_before + '.json')
        fn_dhcp_proc = os.path.join(config.logFilePath, 'dhcp_proc_' + myDate_after + '_' + myDate_before + '.json')
        fn_user_agent = os.path.join(config.logFilePath, 'user_agent_' + myDate_after + '_' + myDate_before + '.json')
        fn_raw_user_agent = os.path.join(config.logFilePath, 'raw_user_agent_' + myDate_after + '_' + myDate_before + '.json')
        fn_assoc_req = os.path.join(config.logFilePath, 'assoc_req_' + myDate_after + '_' + myDate_before + '.json')
        fn_conntrack = os.path.join(config.logFilePath, 'conntrack_' + myDate_after + '_' + myDate_before + '.json')

        res_dhcp_proc = requests.get(url=dhcp_proc, headers=myheaders, params=payload)
        res_dhcp = requests.get(url=dhcp, headers=myheaders, params=payload)
        res_user_agent = requests.get(url=user_agent, headers=myheaders, params=payload)
        res_raw_user_agent = requests.get(url=raw_user_agent, headers=myheaders, params=payload)
        res_assoc_req = requests.get(url=assoc_req, headers=myheaders, params=payload)
        res_conntrack = requests.get(url=conntrack, headers=myheaders, params=payload)
    else:
        print("Getting data without date filter... ")
        fn_dhcp = os.path.join(config.logFilePath, 'dhcp.json')
        fn_dhcp_proc = os.path.join(config.logFilePath, 'dhcp_proc.json')
        fn_user_agent = os.path.join(config.logFilePath, 'user_agent.json')
        fn_raw_user_agent = os.path.join(config.logFilePath, 'raw_user_agent.json')
        fn_assoc_req = os.path.join(config.logFilePath, 'assoc_req.json')
        fn_conntrack = os.path.join(config.logFilePath, 'conntrack.json')

        res_dhcp_proc = requests.get(url=dhcp_proc, headers=myheaders)
        res_dhcp = requests.get(url=dhcp, headers=myheaders)
        res_user_agent = requests.get(url=user_agent, headers=myheaders)
        res_raw_user_agent = requests.get(url=raw_user_agent, headers=myheaders)
        res_assoc_req = requests.get(url=assoc_req, headers=myheaders)
        res_conntrack = requests.get(url=conntrack, headers=myheaders)

    print("res_dhcp status code: " + str(res_dhcp.status_code))
    print("res_dhcp_proc status code: " + str(res_dhcp_proc.status_code))
    print("res_user_agent status code: " + str(res_user_agent.status_code))
    print("assoc_req status code: " + str(res_assoc_req.status_code))
    print("res_dhcp status code: " + str(res_conntrack.status_code))
    print("res_dhcp status code: " + str(res_dhcp.status_code))

    if res_dhcp.status_code == 200:
        with open(fn_dhcp, "w") as f:
            json.dump(res_dhcp.json(), f)
    else:
        print("Could not load res_dhcp!")

    if res_dhcp_proc.status_code == 200:
        with open(fn_dhcp_proc, "w") as f:
            json.dump(res_dhcp_proc.json(), f)
    else:
        print("Could not load res_dhcp_proc!")

    if res_user_agent.status_code == 200:
        with open(fn_user_agent, "w") as f:
            json.dump(res_user_agent.json(), f)
    else:
        print("Could not load res_user_agent!")

    if res_assoc_req.status_code == 200:
        with open(fn_assoc_req, "w") as f:
            json.dump(res_assoc_req.json(), f)
    else:
        print("Could not load res_assoc_req!")

    if res_conntrack.status_code == 200:
        with open(fn_conntrack, "w") as f:
            json.dump(res_conntrack.json(), f)
    else:
        print("Could not load res_conntrack!")

    if res_raw_user_agent.status_code == 200:
        with open(fn_raw_user_agent, "w") as f:
            json.dump(res_raw_user_agent.json(), f)
    else:
        print("Could not load res_raw_user_agent!")

def get_data_intervals_recursive(dateInfo, type='ALL'):
    endDate = dateInfo['endDate']
    if dateInfo['interval'] == None:
        print("Recursion works with interval. No interval is entered. Exiting...")
        exit()
    else:
        interval = int(dateInfo['interval'])
        print("Interval: " + str(interval))
        print("Running recursive get_data..." + str(dateInfo))
        endDateList = []
        endDateList.append(endDate)
        theEnd = datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
        next_endDate = theEnd - timedelta(hours = interval)
        next_endDate = next_endDate.strftime("%Y-%m-%d %H:%M:%S")
        endDateList.append(next_endDate)
        while next_endDate > dateInfo['startDate']:
            theEnd = datetime.strptime(next_endDate, '%Y-%m-%d %H:%M:%S')
            next_endDate = theEnd - timedelta(hours = interval)
            next_endDate = next_endDate.strftime("%Y-%m-%d %H:%M:%S")
            endDateList.append(next_endDate)
        for i,v in enumerate(endDateList):
            thisdateInfo = dateInfo
            thisdateInfo['endDate'] = v
            if thisdateInfo['endDate'] > thisdateInfo['startDate']:
                get_data(thisdateInfo, type='ALL')

def get_ouiList():
    df = pd.read_csv('oui.csv')
    df.set_index('Assignment')
    helper.write_pickle(df, 'ouiList')
    return df