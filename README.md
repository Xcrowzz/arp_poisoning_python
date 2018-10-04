# arp_poisoning_python

## Requirement
python2.7

Get your gateway + iface : 
```bash
?> ip route | grep default
```

## Usage
```bash
?> sudo python2.7 arp_poison.py
```

CTRL+C to stop and write to TARGET_IP_capture.pcac file.

Open pcac in Wireshark and Voila ! 

All your arp caches are belong to us !


# Note
For some reasons, Apple devices under the latest releases tend to interrupt the poisoning. I need to investigate on that, feel free to PR it.
