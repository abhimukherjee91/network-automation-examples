# Subnet Calculater for List of IP addresses

In daily activities in Networking world, sometimes we need individual subnet details for list of IP/Mask. Now, if the number of IPs are less, it is fairely simple to open a subnet calculater online tool and get the subnet of IPs one by one.

But, lets say, if the list of IPs are big and you need to know the subnet details of all those IPs in order to create a ACL or a Prefix-list. In that senario this script might be handy.

All you need to do is to install "ipcalc" python module in your python environment (pip install ipcalc). Once the "ipcalc" is installed, Fill the "networks.csv" file with your IP/Mask details and run the program.

The output file "network_output.csv" file will provide you the Subnet value (Network ID/Mask).
