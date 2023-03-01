import requests
import json
import pandas as pd
import pickle
import os

def write_pickle(data, fileName):
    # print("Writing to pickle!!")
    if fileName.rfind('/')!=-1:
        folderPath = fileName[:fileName.rfind('/')]
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
    filePath = os.path.join(fileName)
    with open(filePath, 'wb') as thefile:
        pickle.dump(data, thefile, protocol=-1)

def read_pickle(fileName):
    # print("Reading from pickle!!")
    filePath = os.path.join(fileName)
    data = []
    if os.path.exists(filePath):
        with open(filePath, 'rb') as thefile:
            data = pickle.load(thefile)
    return data

def get_df(didbName):
    didb_processed = str(didbName) + '_processed'
    if os.path.exists(didb_processed):
        df = read_pickle(didb_processed)
    else:
        df = read_pickle(didbName)
    return df

def update_didb(df, didbName):
    didb_processed = str(didbName) + '_processed'
    write_pickle(df, didb_processed)
    return df

def delete_didb(didbName):
    didb_processed = str(didbName) + '_processed'
    if os.path.exists(didb_processed):
        print("Deleting previous processed didb...")
        os.remove(didb_processed)

def write_df_to_csv(df, filename):
    out = df.to_csv(filename, index=False)
    return out

def unColonizeMAC(mac):
    if not (mac == None):
        themac =  str(mac.replace(":",''))
    else:
        themac = None
    return themac

def colonizeMAC(mac):
    if len(mac.split(':')) == 1:
        themac = ''
        for mi, mv in enumerate(mac):
            themac = themac + mv
            if (mi+1)%2 == 0 and mi < 11:
                themac = themac + ':'
        return themac.lower()
    else:
        return mac
