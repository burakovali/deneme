import json
import pandas as pd
import pickle
import os
import helper, fetcher
import generate
import rules

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