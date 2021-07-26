from netmiko import ConnectHandler
import textfsm

def connect_to_device(ip_address):
    connect = ConnectHandler(device_type='f5_ltm', ip=ip_address, username='root', password='password')
    return connect

device_dictionary = {}
device_dictionary["f5-01"] = "192.168.1.10"
device_dictionary["f5-02"] = "192.168.1.20"



header = "DEVICE_NAME,VS_NAME,VS_IP,VS_PORT,POOL_NAME,POOL_MEMBER_IP,POOL_MEMBER_PORT"

with open("f5_output.csv", 'w') as f:
    f.write(header + "\n")
    f.close()

commands_to_send = """show ltm virtual detail recursive """

for device in device_dictionary:
    print("Starting on device " + device)

    ip_address = device_dictionary[device]
    connection = connect_to_device(ip_address)
    prompt = connection.find_prompt()
    outputs = connection.send_command(commands_to_send)
    outputs = str(outputs)
    
    connection.disconnect()
    with open("f5_tmsh_show_ltm_virtual_detail_recursive.template", 'r') as f:
        template = textfsm.TextFSM(f)
    dicts = template.ParseText(outputs)
    

    for dict in dicts:
        line_to_print = device + ',' + dict[0] + ',' + dict[1] + ',' + dict[2] + ',' + dict[3] + ',' + dict[4] + ',' + dict[5]
        with open("f5_output.csv", 'a') as f:
            f.write(line_to_print + "\n")
    print("Operation completed on " + device)