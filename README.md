# arp_poisoning_python

## 101
Basically, this script uses your iface, gateway and a target IP to fetch every MAC addresses. Once done, it forges ARP requests to poison the target's cache. Then, it sniffes it and writes to a pcap file that can be opened in Wireshark. It doesn't need much resources to run, but the target will feel latencies and can be alerted by any ARP cache monitoring SAS deployed. So, watch out.

## Requirements
python2.7

Unix based system (Or any real OS, get that Windows crap out of your pc folks)

## Usage
Get your gateway + iface : 
```bash
?> ip route | grep default
```

Put those datas in there :
```python
# Parameters                                                                    
gateway_ip = "10.41.254.254"
target_ip = "10.41.254.254"
packet_count = 1000
conf.iface = "wlo1"
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
