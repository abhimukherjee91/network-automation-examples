#Auther: Abhi.Mukherjee

import ipcalc

list = []
with open ("networks.csv",'r') as f:
    for line in f:
        list.append(line.strip())
del list[0]
with open ("networks_output.csv",'w') as f:
    f.write("Input_IP,Subnet" + "\n")
    f.close()
for line in list:
    subnet = ipcalc.Network(line)
    
    print(str(subnet.network()))
    print(str(subnet.subnet()))
    full_subnet = str(subnet.network()) + '/' + str(subnet.subnet())
    line_to_pri = line + ',' + full_subnet
    with open ("networks_output.csv",'a') as f:
        f.write(line_to_pri + "\n")
        f.close()

Print("Completed Sucessfully")





