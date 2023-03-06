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





header_string="00003c00f417b8c743fee6e4e8f88032f417b8c743fe30e3"



def vendor_name_parser(modified):
    list=[]
    processed=re.findall(r'oui=(.*?)\n',modified)
    for current_vendor in processed:
        result=re.search(r"(.*?)\(",current_vendor)
        if("Ieee802.11" not in result.group(1)):
            list.append(result.group(1))
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

def parse_assoc_df(assoc_df):

    ##Remove corrupted assoc data
    assoc_df=assoc_df[~assoc_df['data'].str.contains("sta")]
    assoc_df=assoc_df[~assoc_df['data'].str.contains("Error")]
    ## Add  new columns
    assoc_df["vendors"]=""
    assoc_df['rates']=""
    assoc_df['capabilities']=""
    assoc_df["information_element_id_list"]=""
    assoc_df['spatial_stream']=""
    assoc_df['supported_channel_len']=""
    assoc_df["first_supported_channel"]=""
    assoc_df["supported_channel_raw"]=""
    assoc_df["extended_capabilities_raw"]=""
    assoc_df=assoc_df.reset_index()

    for index,row in assoc_df.iterrows():
    
        #Decode and transform packet into a readable format
        hex_string=header_string+row['data']
        new_packet=bytes.fromhex(hex_string)
        packet=Dot11(_pkt=new_packet)
        build_packet=packet.show(dump=True)
        modified=build_packet.replace(" ","")

        #Parse vendor names
    
        vendor_list=vendor_name_parser(modified)
        assoc_df.at[index,'vendors']=vendor_list

        #Add supported rates

        supported_rates_list=supported_rate_parser(modified)
        assoc_df.at[index,'rates']=supported_rates_list

        ## Add capabilities

        capability_list=capability_parser(modified)
        assoc_df.at[index,"capabilities"]=capability_list


        ## Information Element ID

        information_element_id_list=information_element_id_parser(modified)
        assoc_df.at[index,"information_element_id_list"]=information_element_id_list

            ## Supported Channels
        supported_channel_len=supported_channel_parser(modified)
        assoc_df.at[index,"supported_channel_len"]=supported_channel_len



        ### extra
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
        dot11elt = packet.getlayer(Dot11Elt,ID=36)
        try:
            assoc_df.at[index,"supported_channel_raw"]=dot11elt.info.hex()
            supported_channels=dot11elt.info.hex()
            supported_channel=supported_channels[:2]
            supported_channels_d=int(supported_channel, base=16)
            assoc_df.at[index,"first_supported_channel"]=supported_channels_d
        except:
            pass
        dot11elt = packet.getlayer(Dot11Elt,ID=127)
        try:
            assoc_df.at[index,"extended_capabilities_raw"]=dot11elt.info.hex()
        except:
            pass

        return assoc_df



            




  
    








