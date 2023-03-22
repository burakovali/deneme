import requests
import json
import pandas as pd
import pickle
import os
import helper

# DHCP http://cloud-dpi.herokuapp.com/api/dhcp_processed_api/
# DHCP unprocessed http://cloud-dpi.herokuapp.com/api/dhcp_api/
# Token 71770dd90492c70863464e214113679b3d8bb5ae
# user agent http://cloud-dpi.herokuapp.com/api/identified_devices/
# assoc req http://cloud-dpi.herokuapp.com/api/assoc_req/
# curl --location --request GET 'http://cloud-dpi.herokuapp.com/api/dhcp_processed_api/' --header 'Authorization: Token 71770dd90492c70863464e214113679b3d8bb5ae'

def get_data(type='ALL'):
    if type == 'ALL':
        print("Getting ALL data...")
        dhcp_proc = 'http://cloud-dpi.herokuapp.com/api/dhcp_processed_api/'
        dhcp = 'http://cloud-dpi.herokuapp.com/api/dhcp_api/'
        user_agent = 'http://cloud-dpi.herokuapp.com/api/identified_devices/'
        raw_user_agent = 'https://cloud-dpi.herokuapp.com/api/raw_user_agent/'
        assoc_req = 'http://cloud-dpi.herokuapp.com/api/assoc_req/'
        conntrack = 'https://cloud-dpi.herokuapp.com/api/conntrack_events'
        # payload = { 'key' : 'val' }
        myheaders = {'Authorization': 'Token 71770dd90492c70863464e214113679b3d8bb5ae'}

        res_dhcp_proc = requests.get(url=dhcp_proc, headers=myheaders)
        res_dhcp = requests.get(url=dhcp, headers=myheaders)
        res_user_agent = requests.get(url=user_agent, headers=myheaders)
        res_raw_user_agent = requests.get(url=raw_user_agent, headers=myheaders)
        res_assoc_req = requests.get(url=assoc_req, headers=myheaders)
        res_conntrack = requests.get(url=conntrack, headers=myheaders)

        with open("dhcp.json", "w") as f:
            json.dump(res_dhcp.json(), f)
        with open("dhcp_proc.json", "w") as f:
            json.dump(res_dhcp_proc.json(), f)
        with open("user_agent.json", "w") as f:
            json.dump(res_user_agent.json(), f)
        with open("raw_user_agent.json", "w") as f:
            json.dump(res_raw_user_agent.json(), f)
        with open("assoc_req.json", "w") as f:
            json.dump(res_assoc_req.json(), f)
        with open("conntrack.json", "w") as f:
            json.dump(res_conntrack.json(), f)

def get_ouiList():
    df = pd.read_csv('oui.csv')
    df.set_index('Assignment')
    helper.write_pickle(df, 'ouiList')
    return df