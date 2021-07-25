#!/usr/bin/env python

#Auther: Abhi Mukherjee

import paramiko
import re

#Creating the ESXi Dictionary

device_dictionary = {}
device_dictionary["esxi-01"] = "192.168.1.10"
device_dictionary["esxi-02"] = "192.168.1.20"

username = "root"
password = "password"

# Preparing the Output file

header = "VM_Name,VM_Rule_Count,ESXi_Name,ESXi_Rule_Count"
with open ("VM_ESXi_Rule_Count.csv", 'w') as f:
    f.write(header + "\n")
    f.close()

# Looping through each ESXi to get the host rule count and vnic rule count of each VMs hosted inside

for device in device_dictionary:
    device_ip = device_dictionary[device]
    print("====================starting in " + device + "===================")
    
    # initialize the SSH client

    client = paramiko.SSHClient()

    # add to known hosts

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=device_ip, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server " + device)
        continue

    #Host Rule Count

    stdin, stdout, stderr = client.exec_command('vsipioctl loadruleset | grep Rule.*Count')
    count = re.split(':', stdout.read().decode())[1]
    host_rule_count = count.strip('\n')
    host_rule_count = host_rule_count.strip()
    
    #VM List Preparation

    stdin, stdout, stderr = client.exec_command('esxcli vm process list | grep Name')
    vm_list = []
    for line in stdout.read().decode().splitlines():
        vm_list.append(re.split(':', line)[1])
    
    #getting sfw2 slot details

    for vm in vm_list:
        vm = vm.strip()
        command = 'summarize-dvfilter | grep ' + vm + ' -A 10'
        stdin, stdout, stderr = client.exec_command(command)

        #Getting VM Rule Count

        for line in stdout.read().decode().splitlines():
            if "sfw.2" in line:
                slot_name = re.split(':', line)[1]
                command = 'vsipioctl getrules -f ' + slot_name + ' | wc -l'
                stdin, stdout, stderr = client.exec_command(command)
                vm_rule_count = stdout.read().decode()
                vm_rule_count = vm_rule_count.strip()
               
                line_to_pri = vm + ',' + vm_rule_count + ',' + device + ',' + host_rule_count
                print(line_to_pri)

                with open("VM_ESXi_Rule_Count.csv", 'a') as f:
                    f.write(line_to_pri + "\n")
                    f.close()

    client.close()
    print("================Finished in Device " + device + "====================")



