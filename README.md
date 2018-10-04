# arp_poisoning_python

## 101
Basically, this script uses your iface, gateway and a target IP to fetch every MAC addresses. Once done, it forges ARP requests to poison the target's cache. Then, it sniffes it and writes to a pcap file that can be opened in Wireshark. It doesn't need much resources to run, but the target will feel latencies and can be alerted by any ARP cache monitoring SAS deployed. So, watch out.

## Requirements
python2.7

scapy (https://scapy.net/)

Unix based system (Or any real OS, get that Windows crap out of your pc folks, stay safe!)

(You can easily trick it to work under Windows and OSX, I did not test it though).
Just change : 
```python
    os.system("sysctl -w net.ipv4.ip_forward=0")
```
To enable the ipv4 forwarding on your system (It appears both in the script so watch out).


## Usage
Get your gateway + iface : 
```bash
?> ip route | grep default
```

Put those datas in there :
```python
# Parameters                                                                    
gateway_ip = ""
target_ip = ""
packet_count = 1000
conf.iface = ""
```

Run it :
```bash
?> sudo python2.7 arp_poison.py
```


CTRL+C to stop and write to TARGET_IP_capture.pcac file.

Open pcac in Wireshark and Voila ! 

All your ARP caches are belong to us !


## Notes
For some reasons, Apple devices (under the latest releases) tend to interrupt the poisoning once an authenticated SSL request is made.

I need to investigate on that, feel free to PR it.


# Disclaimer
For educational purposes only (lulz).
