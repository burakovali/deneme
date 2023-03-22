import requests
import json
import pandas as pd
import pickle
import os
import rules
import helper
import assoc_parser, raw_user_agent_parse
from user_agents import parse

def query_by_mac(didbName, mac):
   df = helper.get_merged_df(didbName)
   print(df[df['mac'] == helper.colonizeMAC(mac)])

def query_by_gwmac(didbName, gw_mac):
   df = helper.get_merged_df(didbName)
   print(df[df['gw_mac'].str.contains(helper.colonizeMAC(gw_mac), na=False, case=False)])

def query_by_brand(didbName, brand):
   df = helper.get_merged_df(didbName)
   print(df[df['brand'].str.contains(brand, na=False, case=False)])

def query_by_model(didbName, model):
   df = helper.get_merged_df(didbName)
   print(df[df['model'].str.contains(model, na=False, case=False)])

def query_by_modelVersion(didbName, modelVersion):
   df = helper.get_merged_df(didbName)
   print(df[df['modelVersion'].str.contains(modelVersion, na=False, case=False)])

def query_by_os(didbName, os):
   df = helper.get_merged_df(didbName)
   print(df[df['os'].str.contains(os, na=False, case=False)])

def query_by_osVersion(didbName, osVersion):
   df = helper.get_merged_df(didbName)
   print(df[df['osVersion'].str.contains(osVersion, na=False, case=False)])

def query_by_os(didbName, deviceType):
   df = helper.get_merged_df(didbName)
   print(df[df['deviceType'].str.contains(deviceType, na=False, case=False)])

def query_by_params(didbName, params):
   df = helper.get_merged_df(didbName)
   # params_contraint = (df['params'] == params) | (df['params'].str.contains(params, na=False, case=False))
   print(df[df['params'] == params])

def query_by_timestamp(didbName, start_timestamp, end_timestamp):
   df = helper.get_merged_df(didbName)
   print(df[(df['timestamp'] >= start_timestamp) & (df['timestamp'] <= end_timestamp)])

