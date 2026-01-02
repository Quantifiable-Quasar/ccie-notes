---
layout: default
title: Dual-Hub Dual Cloud DMVPN
parent: 2.3 - FlexVPN, DMVPN, IPsec
---
# Dual-Hub Dual Cloud DMVPN
## Overview

This is very similar to dual-hub single cloud, but the hubs are on separate DMVPN networks. 

<figure class="image"><img style="aspect-ratio:696/296;" src="Dual-Hub Dual Cloud DMVPN_.png" width="696" height="296"></figure>

### Hub

thing

```
hub2#show run int tun 1
Building configuration...

Current configuration : 277 bytes
!
interface Tunnel1
 ip address 10.0.1.1 255.255.255.0
 no ip split-horizon eigrp 1
 ip nhrp authentication Cisco123
 ip nhrp network-id 200
 ip nhrp holdtime 450
 tunnel source GigabitEthernet0/0
 tunnel mode gre multipoint
 tunnel protection ipsec profile ipsec-profile
end

hub2#
```

### Spoke

thing

```
iosv-2#show run int tun 0
Building configuration...

Current configuration : 509 bytes
!
interface Tunnel0
 bandwidth 1000
 ip address 10.0.0.12 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication Cisco123
 ip nhrp map 10.0.0.1 203.0.113.1
 ip nhrp map multicast 203.0.113.1
 ip nhrp map multicast 203.0.113.2
 ip nhrp network-id 100
 ip nhrp holdtime 450
 ip nhrp nhs 10.0.0.1
 ip nhrp nhs 10.0.0.2 nbma 203.0.113.2
 ip nhrp redirect
 ip tcp adjust-mss 1360
 tunnel source GigabitEthernet0/0
 tunnel mode gre multipoint
 tunnel protection ipsec profile ipsec-profile shared
end

iosv-2#show run int tun 1
Building configuration...

Current configuration : 325 bytes
!
interface Tunnel1
 ip address 10.0.1.12 255.255.255.0
 no ip redirects
 ip nhrp authentication Cisco123
 ip nhrp map multicast 203.0.113.2
 ip nhrp network-id 200
 ip nhrp nhs 10.0.1.1 nbma 203.0.113.2
 tunnel source GigabitEthernet0/0
 tunnel mode gre multipoint
 tunnel protection ipsec profile ipsec-profile shared
end

iosv-2# 
```

### Verify

```
iosv-2#show dmvpn
Legend: Attrb --> S - Static, D - Dynamic, I - Incomplete
        N - NATed, L - Local, X - No Socket
        T1 - Route Installed, T2 - Nexthop-override
        C - CTS Capable, I2 - Temporary
        # Ent --> Number of NHRP entries with same NBMA peer
        NHS Status: E --> Expecting Replies, R --> Responding, W --> Waiting
        UpDn Time --> Up or Down Time for a Tunnel
==========================================================================

Interface: Tunnel0, IPv4 NHRP Details 
Type:Spoke, NHRP Peers:2, 

 # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb
 ----- --------------- --------------- ----- -------- -----
     1 203.0.113.1            10.0.0.1  NHRP 00:06:28     S
     1 203.0.113.2            10.0.0.2  NHRP 00:28:30     S

Interface: Tunnel1, IPv4 NHRP Details 
Type:Spoke, NHRP Peers:1, 

 # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb
 ----- --------------- --------------- ----- -------- -----
     1 203.0.113.2            10.0.1.1    UP 00:08:03     S
          
iosv-2#
```