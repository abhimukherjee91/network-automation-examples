import requests
import xml.etree.ElementTree as ET
import os
import getpass
import base64

def create_ouput_file(NSX_Manager):
    op_filename = NSX_Manager + "_Edges_interfaces_details.csv"
    header = "edge_id, Int_Name,connected_with,IPaddr,Mask,isConnected"
    with open (op_filename, 'w') as f:
        f.write(header + "\n")
        f.close()
    return  op_filename

def create_log_file(NSX_Manager):
    log_file = NSX_Manager + "_edge_interface_details_Log.txt"
    with open(log_file, 'w') as f:
        f.close()
    return log_file

def append_to_file(filename, line_to_print):
    with open(filename, 'a') as f:
        f.write(line_to_print + '\n')
        f.close()

# API request Module connection handler wih NSX Manager

def connection(username, passwd, url, log_filename):

    userpass = username + ":" + passwd
    encoded_u = base64.b64encode(userpass.encode()).decode()
    headers = {
        'content-type': "application/xml",
        'authorization': "Basic %s" % encoded_u,

    }
    try:
        response = requests.request("GET", url, headers=headers, verify=False)
        response.raise_for_status()
        append_to_file(log_filename,(url + " ++connection sucess++"))

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
        append_to_file(log_filename, (url + e + " --connection failed--"))

    return response.content

# Function to get the list of nsx edges and it's type

def nsx_edge_list(NSX_Manager,username,passwd,log_filename):
    url = "https://" + NSX_Manager + "/api/4.0/edges"
    edge_dict = {}
    response = connection(username, passwd, url,log_filename)
    tree = ET.fromstring(response)[0]

    for edge_id in tree.findall("edgeSummary"):
        for edge_type in edge_id.findall("edgeType"):
            edge_dict[edge_id[0].text] = edge_type.text

    append_to_file(log_filename, "++ nsx_edge_list_prepared ++ ")
    return edge_dict


# Edge_type = DLR interface details

def nsx_edge_dlr_int_details(edge_id,NSX_Manager,username,passwd,op_filename,log_filename):
    url = "https://" + NSX_Manager + "/api/4.0/edges/" + edge_id + "/interfaces"
    response = connection(username, passwd, url,log_filename)
    tree = ET.fromstring(response)
    for vnic in tree.findall('interface'):
        vnic_name = vnic.find('name').text
        vnic_ip_addr = vnic.find('addressGroups/addressGroup/primaryAddress').text
        vnic_ip_mask = vnic.find('addressGroups/addressGroup/subnetMask').text
        vnic_connected_with = vnic.find('connectedToName').text
        vnic_connected_status = vnic.find('isConnected').text
        line_to_print = edge_id + ',' + vnic_name + ',' + vnic_connected_with + ',' + vnic_ip_addr + ',' + vnic_ip_mask+\
                        ',' + vnic_connected_status
        append_to_file(op_filename,line_to_print)
        append_to_file(log_filename, ('--worked on ' + edge_id + ' ' + vnic_name + " --"))

def nsx_edge_esg_int_details(edge_id,NSX_Manager,username,passwd,op_filename,log_filename):
    url = "https://" + NSX_Manager + "/api/4.0/edges/" + edge_id + "/vnics"
    response = connection(username, passwd, url,log_filename)
    tree = ET.fromstring(response)
    for vnic in tree.findall('vnic'):
        if (vnic.find('isConnected').text) == 'true':
            vnic_name = (vnic.find('name').text).strip()
            vnic_connected_status = vnic.find('isConnected').text
            vnic_connected_with = vnic.find('portgroupName').text
            vnic_primary_addrs = vnic.findall('addressGroups/addressGroup')
            for vnic_primary_addr in vnic_primary_addrs:
                vnic_pri_ip = vnic_primary_addr.find('primaryAddress').text
                vnic_pri_mask = vnic_primary_addr.find('subnetMask').text
                line_to_print = edge_id + ',' + vnic_name + ',' + vnic_connected_with + ',' + vnic_pri_ip + ',' + \
                                vnic_pri_mask + ',' + vnic_connected_status
                append_to_file(op_filename,line_to_print)
                append_to_file(log_filename, ('--worked on ' + edge_id + ' ' + vnic_name + " --"))

def get_nsx_edge_interface(NSX_Manager,username,passwd):

    op_filename = create_ouput_file(NSX_Manager)
    log_filename = create_log_file(NSX_Manager)

    edge_dict = nsx_edge_list(NSX_Manager,username,passwd,log_filename)

    for key in edge_dict.keys():

        if edge_dict[key] == 'distributedRouter':
            append_to_file(log_filename, ('++ Started working on edge ' + key + ' ++'))
            nsx_edge_dlr_int_details(key,NSX_Manager,username,passwd,op_filename,log_filename)
            append_to_file(log_filename, ('++ Finished working on edge ' + key + ' ++'))

        elif edge_dict[key] == "gatewayServices":
            append_to_file(log_filename, ('++ Started working on edge ' + key + ' ++'))
            nsx_edge_esg_int_details(key,NSX_Manager,username,passwd,op_filename,log_filename)
            append_to_file(log_filename, ('++ Finished working on edge ' + key + ' ++'))

if __name__ == "__main__":
    get_nsx_edge_interface()