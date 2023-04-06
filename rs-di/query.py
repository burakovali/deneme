import requests
import json
import pandas as pd
import pickle
import os
import rules
import helper
import assoc_parser, raw_user_agent_parse
from user_agents import parse

def query_by_mac(mac):
   df = helper.get_combined_df()
   print(df[df['mac'] == helper.colonizeMAC(mac)])
   return df[df['mac'] == helper.colonizeMAC(mac)]

def query_by_gwmac(gw_mac):
   df = helper.get_combined_df()
   print(df[df['gw_mac'].str.contains(helper.colonizeMAC(gw_mac), na=False, case=False)])
   return df[df['gw_mac'].str.contains(helper.colonizeMAC(gw_mac), na=False, case=False)]

def query_by_brand(brand):
   df = helper.get_combined_df()
   print(df[df['brand'].str.contains(brand, na=False, case=False)])
   return df[df['brand'].str.contains(brand, na=False, case=False)]

def query_by_model(model):
   df = helper.get_combined_df()
   print(df[df['model'].str.contains(model, na=False, case=False)])
   return df[df['model'].str.contains(model, na=False, case=False)]

def query_by_modelVersion(modelVersion):
   df = helper.get_combined_df()
   print(df[df['modelVersion'].str.contains(modelVersion, na=False, case=False)])
   return df[df['modelVersion'].str.contains(modelVersion, na=False, case=False)]

def query_by_os(os):
   df = helper.get_combined_df()
   print(df[df['os'].str.contains(os, na=False, case=False)])
   return df[df['os'].str.contains(os, na=False, case=False)]

def query_by_osVersion(osVersion):
   df = helper.get_combined_df()
   print(df[df['osVersion'].str.contains(osVersion, na=False, case=False)])
   return df[df['osVersion'].str.contains(osVersion, na=False, case=False)]

def query_by_deviceType(deviceType):
   df = helper.get_combined_df()
   print(df[df['deviceType'].str.contains(deviceType, na=False, case=False)])
   return df[df['deviceType'].str.contains(deviceType, na=False, case=False)]

def query_by_params(params):
   df = helper.get_combined_df()
   # params_contraint = (df['params'] == params) | (df['params'].str.contains(params, na=False, case=False))
   print(df[df['params'] == params])
   return df[df['params'] == params]

def query_by_timestamp(start_timestamp, end_timestamp):
   df = helper.get_combined_df()
   print(df[(df['timestamp'] >= start_timestamp) & (df['timestamp'] <= end_timestamp)])
   return df[(df['timestamp'] >= start_timestamp) & (df['timestamp'] <= end_timestamp)]

