import json
import pandas as pd
import pickle
import os
import helper, fetcher
import generate
import rules
import math

def analyze_didb(didbName='didb', write_to_file=True):
    df = helper.get_merged_df(didbName)

    all = len(df)
    nobrand = len(df[df['brand'] == ''])
    brand_matching = round(100*(all - nobrand)/all,1)
    nomodel = len(df[df['model'] == ''])
    model_matching = round(100*(all - nomodel)/all,1)
    nomodelVersion = len(df[df['modelVersion'] == ''])
    modelVersion_matching = round(100*(all - nomodelVersion)/all,1)
    noos = len(df[df['os'] == ''])
    os_matching = round(100*(all - noos)/all,1)
    noosVersion = len(df[df['osVersion'] == ''])
    osVersion_matching = round(100*(all - noosVersion)/all,1)
    nodeviceType = len(df[df['deviceType'] == ''])
    deviceType_matching = round(100*(all - nodeviceType)/all,1)

    print('All:' + str(all) + ', No brand:' + str(nobrand) + " -> Brand matching: " + str(brand_matching) +'%')
    print('All:' + str(all) + ', No model:' + str(nomodel) + " -> Model matching: " + str(model_matching) +'%')
    print('All:' + str(all) + ', No modelVersion:' + str(nomodelVersion) + " -> Model Version matching: " + str(modelVersion_matching) +'%')
    print('All:' + str(all) + ', No os:' + str(noos) + " -> OS matching: " + str(os_matching) +'%')
    print('All:' + str(all) + ', No osVersion:' + str(noosVersion) + " -> OS Version matching: " + str(osVersion_matching) +'%')
    print('All:' + str(all) + ', No deviceType:' + str(nodeviceType) + " -> Device Type matching: " + str(deviceType_matching) +'%')
## Function to concanate all values
def concanate(x):
    current_string=''
    for data_point in x:
        if data_point is not None :
            try:
                current_string=current_string+data_point
            except:
                pass  
    return current_string

        
    
def count_missing_values(didbName='didb', write_to_file=True):
    df=helper.get_df(didbName)
    ## Remove some problematic data points
    df.loc[df['vendor'] == 'None', 'vendor'] = ''
    df.loc[df['vendor']== 'nan', 'vendor'] = ''
    ## Merged to find missing values
    df=df.groupby(["mac"], as_index=False).agg({'user_agent':lambda x:concanate(x),'hostname':lambda x:concanate(x),'params':lambda x:concanate(x),'vendor':lambda x:concanate(x),'assoc_req_spatial_stream':'sum','assoc_req_vendors':lambda x:concanate(x),'wfa_device_name':lambda x:concanate(x)})

    ##Get the count of missing values
    user_agent = len(df[df['user_agent'] == ''])
    hostname = len(df[df['hostname'] == ''])
    params = len(df[df['params'] == ''])
    vendor = len(df[df['vendor'] == ''])
    hostname_useragent=len(df[ (df['hostname'] == '') & (df['user_agent']== '')])
    assoc_req_spatial_stream = len(df[df['assoc_req_spatial_stream'] == 0])
    assoc_req_vendors = len(df[df['assoc_req_vendors'] == ''])
    wfa_device_name= len(df[df['wfa_device_name'] == ''])
    
    print('There are '+str(len(df))+' unique mac addresses')
    print(str(user_agent)+" of them are missing user agent| %"+str(100*(len(df) - user_agent)/len(df)))
    print(str(hostname)+" of them are missing hostname| %"+str(100*(len(df) - hostname)/len(df)))
    print(str(params)+" of them are missing params| %"+str(100*(len(df) - params)/len(df)))
    print(str(vendor)+" of them are missing vendor| %"+str(100*(len(df) - vendor)/len(df)))
    print(str(assoc_req_spatial_stream)+" of them are missing assoc request| %"+str(100*(len(df) - assoc_req_spatial_stream)/len(df)))
    print(str(assoc_req_vendors)+" of them are missing assoc request vendor| %"+str(100*(len(df) - assoc_req_vendors)/len(df)))
    print(str(wfa_device_name)+" of them are missing wfa device name| %"+str(100*(len(df) - wfa_device_name)/len(df)))
    print(str(hostname_useragent)+ " of them are missing both hostname and user_agent| % "+  str(100-100*(len(df) - hostname_useragent)/len(df)))
