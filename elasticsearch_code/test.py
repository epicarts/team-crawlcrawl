#!/usr/bin/python

import json
import subprocess
import sys

CONTAINER = sys.argv[1]
print(CONTAINER)
# Inspecting container via Subprocess
proc = subprocess.Popen(["docker","inspect",CONTAINER],
                      stdout=subprocess.PIPE,
                      stderr=subprocess.STDOUT)

out = proc.stdout.read()
json_data = json.loads(out)[0]

net_dict = {}
for network in json_data["NetworkSettings"]["Networks"].keys():
    net_dict['mac_addr']  = json_data["NetworkSettings"]["Networks"][network]["MacAddress"]
    net_dict['ipv4_addr'] = json_data["NetworkSettings"]["Networks"][network]["IPAddress"]
    net_dict['ipv4_net']  = json_data["NetworkSettings"]["Networks"][network]["IPPrefixLen"]
    net_dict['ipv4_gtw']  = json_data["NetworkSettings"]["Networks"][network]["Gateway"]
    net_dict['ipv6_addr'] = json_data["NetworkSettings"]["Networks"][network]["GlobalIPv6Address"]
    net_dict['ipv6_net']  = json_data["NetworkSettings"]["Networks"][network]["GlobalIPv6PrefixLen"]
    net_dict['ipv6_gtw']  = json_data["NetworkSettings"]["Networks"][network]["IPv6Gateway"]
    for item in net_dict:
        if net_dict[item] == "" or net_dict[item] == 0:
            net_dict[item] = "null"
    print ("\n[%s]" % network)
    print ("\n{}{:>13} {:>14}".format(net_dict['mac_addr'],"IP/NETWORK","GATEWAY"))
    print ("--------------------------------------------")
    print ("IPv4 settings:{:>16}/{:<5}  {}".format(net_dict['ipv4_addr'],net_dict['ipv4_net'],net_dict['ipv4_gtw']))
    print ("IPv6 settings:{:>16}/{:<5}  {}".format(net_dict['ipv6_addr'],net_dict['ipv6_net'],net_dict['ipv6_gtw']))