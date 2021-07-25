#!/usr/bin/env python

#Auther: Abhi Mukherjee


import pyeapi

# Creating Device Dictonary

device_dictionary = {}
device_dictionary["eos-sw-01"] = "192.168.1.10"
device_dictionary["eos-sw-02"] = "192.168.1.20"

# Preparing the output File

header = "Switch_Name,VLAN, MAC-ADDR, Interface"
with open ("Arista_MAC_Add_table.csv" , 'w') as f:
    f.write(header + "\n")
    f.close()

#Loop to get the data from the device and append the output file

for device in device_dictionary:
    device_ip = device_dictionary[device]
    print("starting in " + device)

    node = pyeapi.connect(transport='https', host=device_ip, username='admin', password='password',
                          return_node=True)
    outputs = node.enable(['show mac address-table dynamic'])
    for output in outputs[0]['result']['unicastTable']['tableEntries']:
        line_to_print = device + "," + str(output['vlanId']) + "," + str(output['macAddress']) + "," + str(output['interface'])
        print(line_to_print)
        with open("Arista_MAC_Add_table.csv", 'a') as f:
            f.write(line_to_print + "\n")
            f.close()



   


