import argparse
import os
from time import sleep
import sys
from scapy.utils import RawPcapReader
from scapy.layers.dot11 import *
from scapy.packet import Packet
from scapy.all import *
import re
import pandas as pd
import json
import numpy as np





header_string="00003c00f417b8c743fee6e4e8f88032f417b8c743fe30e3"



def vendor_name_parser(modified):
    list=[]
    try:
        processed=re.findall(r'oui=(.*?)\n',modified)
        for current_vendor in processed:
            result=re.search(r"(.*?)\(",current_vendor)
            if("Ieee802.11" not in result.group(1)):
                list.append(result.group(1))
    except:
        list=[None]
    return list

def supported_rate_parser(modified):
    processed=re.findall(r'rates=(.*?)\n',modified)
    return processed

def capability_parser(modified):
    processed=re.findall(r'cap=(.*?)\n',modified)
    return processed

def supported_channel_parser(modified):
    
    processed=re.findall(r'ID=SupportedChannels\nlen=(.*?)\n',modified,re.M)
    return processed

def information_element_id_parser(modified):
    processed=re.findall(r'###\[802.11InformationElement\]###\nID=(.*?)\n',modified,re.M)
    return processed

def parse_assoc_df(assoc_df2):
    assoc_df = pd.json_normalize(assoc_df2)
 

    ##Remove corrupted assoc data
    assoc_df=assoc_df[~assoc_df['data'].str.contains("sta")]
    assoc_df=assoc_df[~assoc_df['data'].str.contains("Error")]
    assoc_df.dropna( axis=0,subset=None, inplace=True)
    ## Add  new columns
    assoc_df["vendors"]=""
    assoc_df['spatial_stream']=""
    assoc_df['wfa_device_name']=""
    assoc_df=assoc_df.reset_index()

    for index,row in assoc_df.iterrows():
 
        wfa_device_name_list=[]
        #Decode and transform packet into a readable format
        hex_string=header_string+row['data']
        new_packet=bytes.fromhex(hex_string)
        packet=Dot11(_pkt=new_packet)
        build_packet=packet.show(dump=True)
        modified=build_packet.replace(" ","")

        #Vendor Name List

        vendor_list=vendor_name_parser(modified)
        assoc_df.at[index,'vendors']=vendor_list


        ### Spatial Stream
        dot11elt = packet.getlayer(Dot11Elt,ID=45)
        try:
            element_value=str(dot11elt.info.hex())[6:26]
            element_int_value = int(element_value, base=16)
            element_binary_value = str(bin(element_int_value))[2:]
            first_unsported_mcs=element_binary_value.index("0")
            if first_unsported_mcs == 8:
                assoc_df.at[index,"spatial_stream"]=1
            elif first_unsported_mcs == 16:
                assoc_df.at[index,"spatial_stream"]=2
            else:
                assoc_df.at[index,"spatial_stream"]=3        
        except:
            pass


        try:
            dot11elt = packet.getlayer(Dot11Elt,ID=221)
            while dot11elt :
                if(int(str(dot11elt.info.hex())[6:8], base=16)==9):
                    wfa_device_name_list.append(bytes.fromhex((str(dot11elt.info.hex())[66:])).decode("ASCII"))
                    break
                dot11elt = dot11elt.payload.getlayer(Dot11Elt)
        except:
            pass

        if wfa_device_name_list:
                assoc_df.at[index,"wfa_device_name"] = wfa_device_name_list
        else :
                assoc_df.at[index,"wfa_device_name"] = [None]

                
   ##Temporarily converting to list of list for effiency

    assoc_df=assoc_df.groupby(["device_mac", "gw_mac"], as_index=False).agg({'timestamp':'first', 'spatial_stream':'first', 'vendors':lambda value:str(set([item for sublist in value for item in sublist])),'wfa_device_name':lambda value:str(set([item for sublist in value for item in sublist]))})
    assoc_json= json.loads(assoc_df.to_json(orient = 'records'))

    return assoc_json



            




  
    








