#Auther: Abhi Mukherjee
## This script provides you individual configuration of NSX-T Gateway Firewall rules in JSON format. It creates 2
## files. "Policy" one provides you the Name and Path for individual policies and the "Rules" file provides you the json
##of individual rules under each policy.

#usage: python3 GW-FW-Rule-Extract.py

import requests
import json
import calendar
import time
import base64

def getconnection(manager,uri,auth):
    headers = {
        'content-type': "application/json",
        'authorization': "Basic %s" % auth,
    }
    url="https://"+manager+"/policy/api/v1"+uri
    # print(url)
    try:
        response=requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    return response.json()

def gw_fw_domains(manager,auth):
    uri="/infra/domains/"
    domains=getconnection(manager,uri,auth)
    domain_list =[]
    for domain in domains['results']:
        domain_list.append(domain['path'])
    return domain_list

def gw_policies(manager,auth,fw_domain):
    gw_policies=getconnection(manager,fw_domain,auth)
    gw_policy_dict={}
    for gw_policy in gw_policies['results']:
        gw_policy_dict[(gw_policy['display_name'])] = gw_policy['path']
    return gw_policy_dict

def append_file(filename,line_to_print):
    with open (filename, 'a') as f:
        f.write(line_to_print+ '\n')
        f.close()

def main():
    manager=input("Manager IP: ")
    user=input("USername: ")
    passwd=input("Password: ")
    userpass = user + ":" + passwd
    auth=base64.b64encode(userpass.encode()).decode()
    gw_fw_rule_filename="GW_FW_Rules_"+str(calendar.timegm((time.gmtime())))+".txt"
    gw_fw_policy_filename = "GW_FW_policy_" + str(calendar.timegm((time.gmtime()))) + ".txt"
    with open(gw_fw_rule_filename, 'w') as f:
        f.close()
    with open(gw_fw_policy_filename, 'w') as f:
        f.close()
    fw_domins=gw_fw_domains(manager,auth)
    for fw_domain in fw_domins:
        gw_policies_dict=gw_policies(manager, auth, (fw_domain+"/gateway-policies"))
        for policy_key, policy_path in gw_policies_dict.items():
            line_to_pri=policy_key+":"+policy_path
            append_file(gw_fw_policy_filename,line_to_pri)

        for key in gw_policies_dict.keys():
            gw_policy_rule_uri=gw_policies_dict[key]+"/rules"
            gw_policy_rules=getconnection(manager,gw_policy_rule_uri,auth)
            for rule in gw_policy_rules['results']:
                append_file(gw_fw_rule_filename, ("+"*20))
                append_file(gw_fw_rule_filename, key)
                append_file(gw_fw_rule_filename, ("="*10))
                append_file(gw_fw_rule_filename, str(rule))


if __name__ == "__main__":
    main()
