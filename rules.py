import requests
import json
import pandas as pd
import pickle
import os
import helper
import rules_brand, rules_model, rules_modelVersion, rules_os, rules_osVersion, rules_deviceType

# brand_rules = [rules_brand.mark_brand_apple, rules_brand.mark_brand_samsung, rules_brand.mark_brand_hp, rules_brand.mark_brand_airties, rules_brand.mark_brand_huawei, rules_brand.mark_brand_xiaomi, rules_brand.mark_brand_lenovo, rules_brand.mark_brand_nintendo]
brand_rules = [rules_brand.mark_brand_apple, rules_brand.mark_brand_samsung, rules_brand.mark_brand_hp,
               rules_brand.mark_brand_airties, rules_brand.mark_brand_huawei, rules_brand.mark_brand_xiaomi,
               rules_brand.mark_brand_lenovo, rules_brand.mark_brand_sony, rules_brand.mark_brand_nintendo,
               rules_brand.mark_brand_oui]
# model_rules = [rules_model.mark_model_iphone, rules_model.mark_model_macBook, rules_model.mark_model_macBookPro, rules_model.mark_model_galaxy, rules_model.mark_model_galaxyTab, rules_model.mark_model_hpPrinter, rules_model.mark_model_nintendo]
model_rules =[rules_model.mark_model_iphone, rules_model.mark_model_ipad, rules_model.mark_model_ipadPro,
                rules_model.mark_model_macBook, rules_model.mark_model_macBookPro, rules_model.mark_model_galaxy,
                rules_model.mark_model_galaxyTab, rules_model.mark_model_hpPrinter, rules_model.mark_model_thinkpad,
               rules_model.mark_model_elitebook, rules_model.mark_model_huaweiP, rules_model.mark_model_xiaomiMi,
               rules_model.mark_model_mediapad, rules_model.mark_model_playStation, rules_model.mark_model_air4960,
               rules_model.mark_model_air4443, rules_model.mark_model_nintendo]
modelVersion_rules = [rules_modelVersion.mark_modelVersion_galaxy, rules_modelVersion.mark_modelVersion_galaxyTab,
                      rules_modelVersion.mark_modelVersion_xiaomiMi, rules_modelVersion.mark_modelVersion_mediaPad,
                      rules_modelVersion.mark_modelVersion_ThinkPad]

# os_rules = [rules_os.mark_os_mac, rules_os.mark_os_iphone, rules_os.mark_os_android, rules_os.mark_os_windows, rules_os.mark_os_linux]
os_rules = [rules_os.mark_os_appleTV, rules_os.mark_os_iphone, rules_os.mark_os_mac,
            rules_os.mark_os_android, rules_os.mark_os_linux, rules_os.mark_os_nintendo3SDSS,
            rules_os.mark_os_windows, rules_os.mark_os_ipad, rules_os.mark_os_unix]

osVersion_rules = [rules_osVersion.mark_ios_version, rules_osVersion.mark_android_version, rules_osVersion.mark_windows_version, rules_osVersion.mark_macos_version, rules_osVersion.mark_modelVersion_appleOS_generic]
deviceType_rules = [rules_deviceType.mark_deviceType_mobile, rules_deviceType.mark_deviceType_laptop, rules_deviceType.mark_deviceType_gamingConsole, rules_deviceType.mark_deviceType_tv, rules_deviceType.mark_deviceType_tablet]

# all_rules = [brand_rules, model_rules, modelVersion_rules, os_rules, osVersion_rules, deviceType_rules]
all_rules = [model_rules, os_rules, brand_rules, modelVersion_rules, osVersion_rules, deviceType_rules]