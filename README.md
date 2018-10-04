# arp_poisoning_python

Requirement : python2.7

Get your gateway + iface : ?> ip route | grep default

Usage : sudo python2.7 arp_poison.py

CTRL+C to stop and write to TARGET_IP_capture.pcac file.

Open pcac in Wireshark and Voila, the arp cache of your target is fucked up. 



# Note
For some reasons, Apple devices under the latest releases tend to interrupt the poisoning. I need to investigate on that, feel free to PR it.
