#f5 Examples:

For accessing f5 devices I have mostly used netmiko and to parse the text data I have used textfsm instead of regular re.

To install these 2 modules:

pip install netmiko
pip install text-fsm

Inside the python files, just edit it to put your device's ip address in the device_dictonary and replace the credentials with your creds.