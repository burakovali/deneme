import requests
import json
import pandas as pd
import pickle
import os
import helper


def mark_deviceType_mobile(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    df.loc[(df['OS'] == 'iOS'), 'type'] = 'Mobile'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df


def mark_deviceType_laptop(didbName='didb', write_to_file=True):
    df = helper.get_df(didbName)
    df.loc[(df['model'] == 'macBook') | (df['model'] == 'macBookPro'), 'type'] = 'Laptop'
    if write_to_file:
        helper.update_didb(df, didbName)
    return df
    