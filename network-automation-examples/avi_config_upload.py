#!/usr/bin/env python

#Auther: Abhi Mukherjee

"""
This program will be usuful when you have converted f5/Netsclar/NSX-T configuration to json formatted AVI config using the f5_converter/netsclater_converter utility (cli-upload option).
This is because you wanted to modify the converted config (i.e. VS name change, IP change etc) before sending it to the AVI controller.
After you modify the JSON formatted AVI conig file, use this program to upload the config file to AVI controller

Usage:
 python3 avi_config_upload.py --f ./test/ns-Output.json -u <username> -p <password> -t <tanent> -c <controller_ip> --controller_version <controller_version>
 
"""

from avi.migrationtools import avi_rest_lib
import json
import argparse

def config_upload(args):
    avi_config_file = args.f
    avi_controller_ip = args.controller_ip
    avi_username = args.user
    avi_passowrd = args.password
    avi_version= args.controller_version
    avi_tenant = args.tenant
        
    with open (avi_config_file) as json_file:
        avi_config_dict = json.load(json_file)
    
    try:
        avi_rest_lib.upload_config_to_controller(avi_config_dict, avi_controller_ip, avi_username, avi_passowrd, avi_tenant)
    except:
        print("!!!!Exception Occured!!!!")
        exit()
    else:
        print("####Config Uploaded to AVI Controller####")
    


parser = argparse.ArgumentParser()
        
        
parser.add_argument('--f', help='absolute path of avi json file')

parser.add_argument('-u', '--user',
                        help='controller username for auto upload',
                        default='admin')
                        
parser.add_argument('-p', '--password',
                        help='controller password for config upload.')
                                        

parser.add_argument('--controller_version',
                        help='Target Avi controller version')
                        
parser.add_argument('-t', '--tenant',
                        help='tenant name for auto upload',
                        default='admin')

parser.add_argument('-c', '--controller_ip',
                        help='controller ip for auto upload')

args = parser.parse_args()
print("####Sending Config to AVI Controller####")
configuration_upload = config_upload(args)





                        
