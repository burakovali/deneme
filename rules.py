import requests
import json
import pandas as pd
import pickle
import os
import helper
import rules_brand, rules_model, rules_modelVersion, rules_os, rules_osVersion, rules_deviceType

brand_rules = [rules_brand.mark_brand_apple, rules_brand.mark_brand_samsung, rules_brand.mark_brand_hp, rules_brand.mark_brand_airties, rules_brand.mark_brand_huawei, rules_brand.mark_brand_xiaomi, rules_brand.mark_brand_lenovo, rules_brand.mark_brand_nintendo]
model_rules = [rules_model.mark_model_iphone, rules_model.mark_model_macBook, rules_model.mark_model_macBookPro, rules_model.mark_model_galaxy, rules_model.mark_model_galaxyTab, rules_model.mark_model_hpPrinter, rules_model.mark_model_nintendo]
modelVersion_rules = [rules_modelVersion.mark_modelVersion_galaxy, rules_modelVersion.mark_modelVersion_galaxyTab]
os_rules = [rules_os.mark_os_mac, rules_os.mark_os_iphone, rules_os.mark_os_android, rules_os.mark_os_windows, rules_os.mark_os_linux]
osVersion_rules = [rules_osVersion.mark_ios_version, rules_osVersion.mark_android_version, rules_osVersion.mark_windows_version]
deviceType_rules = [rules_deviceType.mark_deviceType_mobile, rules_deviceType.mark_deviceType_laptop]

all_rules = [brand_rules, model_rules, modelVersion_rules, os_rules, osVersion_rules, deviceType_rules]
