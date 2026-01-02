---
layout: default
title: Dual Hub DMVPN
parent: 2.3 - FlexVPN, DMVPN, IPsec
---
# Dual Hub DMVPN
## Overview

This will use the same network as the previous DMPVN, but a new router will be added to be the second hub. 

<figure class="image"><img style="aspect-ratio:514/218;" src="Dual Hub DMVPN_image.png" width="514" height="218"></figure>

### Configuring Hub2

thing

```
hub2(config)#interface Tunnel0
hub2(config-if)#bandwidth 1000
hub2(config-if)#ip address 10.0.0.2 255.255.255.0
hub2(config-if)#no ip redirects
hub2(config-if)#no ip split-horizion eigrp 1
hub2(config-if)#ip mtu 1400
hub2(config-if)#ip nhrp authentication Cisco123
hub2(config-if)#ip nhrp network-id 100
hub2(config-if)#ip nhrp holdtime 450
hub2(config-if)#ip tcp adjust-mss 1360
hub2(config-if)#tunnel source GigabitEthernet0/0
hub2(config-if)#tunnel mode gre multipoint
hub2(config-if)#tunnel protection ipsec profile ipsec-profile
hub2(config-if)#ip nhrp map 10.0.0.1 203.0.113.1
hub2(config-if)#ip nhrp map multicast 203.0.113.1
hub2(config-if)#ip nhrp nhs 203.0.113.1
hub2(config-if)#
```

### Configuring the spokes

thing

```
iosv-1(config)#int tunnel 1
iosv-1(config-if)#ip nhrp map 10.0.0.2 203.0.113.2
iosv-1(config-if)#ip nhrp map multicast 203.0.113.2
iosv-1(config-if)#ip nhrp nhs 203.0.113.2
iosv-1(config-if)#
```