import requests, socket
import pandas as pd
import json
import re
import helper

from http.server import BaseHTTPRequestHandler
from io import BytesIO



class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

def regex_parse(data_str): ##parse raw data with regex

    modified=data_str[3:len(data_str)-1].replace("\\r\\n","|||")
    processed=re.findall(r'User-Agent:(.*?)\|',modified,re.M)

    if len(processed)>0:
        return processed[0]
    else:
        return ''
    

def http_parse(data_str): ## Search get and post parse with Httprequest library 
    httpstartindex = data_str.find('474554')
    if httpstartindex == -1:
        httpstartindex = data_str.find('484541')
    try:
        httprequestbytes = data_str[httpstartindex:]
        httprequestbytes = bytes.fromhex(httprequestbytes)
        request = HTTPRequest(httprequestbytes)
        return request.headers['User-Agent'] 
    except:
        return ''

def parse_user_agent(raw_data):
    raw_user_agent_df = pd.json_normalize(raw_data)
    raw_user_agent_df.rename({'device_mac': 'mac'}, axis=1, inplace=True)
    raw_user_agent_df['user_agent']=''
    for index,row in raw_user_agent_df.iterrows():
        raw_user_agent_df.loc[index, 'mac'] = helper.unColonizeMAC(row['mac'])
        try:
            raw_user_agent_df.at[index,'user_agent']=regex_parse(str(bytes.fromhex(row['data'])))  # "cm.bell-labs.com"
        except Exception as e:
            raw_user_agent_df.at[index,'user_agent']=''

 
    raw_user_agent_df.to_csv("raw_user_agent.csv")    
    raw_user_agent_json= json.loads(raw_user_agent_df.to_json(orient = 'records'))
    return raw_user_agent_json

