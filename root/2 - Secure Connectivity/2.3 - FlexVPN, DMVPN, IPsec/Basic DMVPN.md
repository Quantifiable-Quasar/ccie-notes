---
layout: default
title: Basic DMVPN
parent: 2.3 - FlexVPN, DMVPN, IPsec
---
# Basic DMVPN
[https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec\_conn\_dmvpn/configuration/15-mt/sec-conn-dmvpn-15-mt-book/sec-conn-dmvpn-dmvpn.html](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/15-mt/sec-conn-dmvpn-15-mt-book/sec-conn-dmvpn-dmvpn.html)

## Overview

DMVPN is the next evolution of VPN technology. It works with IPsec, Next Hop Router Protocol (NHRP), and multipoint Generic Routing and Encapsulation (mGRE). NHRP creates mappings between overlay and underlay addresses, and mGRE allows for one tunnel interface to open an arbitrary number of tunnels. This allows for on-demand spoke-to-spoke tunnel creation. 

<figure class="image"><img style="aspect-ratio:744/339;" src="Basic DMVPN_image.png" width="744" height="339"></figure>

1.  Configure IPsec profile
2.  Configure the hub
3.  Configure the spoke
4.  Configure dynamic routing

### Configure IPsec profile

This is a template IPsec profile that can be placed on all four routers. It's pretty wide open, but typically it would be more locked down.

```
iosv-0(config-if)#crypto ikev2 keyring ike-keyring
iosv-0(config-ikev2-keyring)#peer dmvpn
iosv-0(config-ikev2-keyring-peer)#address 0.0.0.0 0.0.0.0 
iosv-0(config-ikev2-keyring-peer)#pre-shared-key Cisco123
iosv-0(config-ikev2-keyring-peer)#exit
iosv-0(config-ikev2-keyring)#crypto ikev2 profile ike-profile
IKEv2 profile MUST have:
   1. A local and a remote authentication method.
   2. A match identity or a match certificate or match any statement.
iosv-0(config-ikev2-profile)#authentication local pre-share
iosv-0(config-ikev2-profile)#authentication remote pre-share
iosv-0(config-ikev2-profile)#keyring local ike-keyring
iosv-0(config-ikev2-profile)#match address local interface g0/0
iosv-0(config-ikev2-profile)#match identity remote address 0.0.0.0 0.0.0.0
iosv-0(config-ikev2-profile)#exit
iosv-0(config)#crypto ipsec profile ipsec-profile
iosv-0(ipsec-profile)#set ikev2-profile ike-profile
iosv-0(ipsec-profile)#exit
iosv-0(config)#
```

### Configure hub

Once the IPsec profile is configured, the tunnel interface can be set up. The three NHRP commands specify the password and the network id. The map multicase dynamic command allows for spokes to register themselves in the NHRP database. The tunnel mode is set the same way as a typical IPsec deployment, but the mode is set to mGRE to allow for dynamic tunnel creation. 

```
iosv-0(config)#int tunnel 0        
iosv-0(config-if)#ip address 10.0.0.1 255.255.255.0
iosv-0(config-if)#ip mtu 1400
iosv-0(config-if)#ip nhrp authentication Cisco123
iosv-0(config-if)#ip nhrp map multicast dynamic
iosv-0(config-if)#ip nhrp network-id 100
iosv-0(config-if)#tunnel source g0/0 
iosv-0(config-if)#tunnel mode gre multipoint
iosv-0(config-if)#tunnel protection ipsec profile ipsec-profile
iosv-0(config-if)#bandwidth 1000
iosv-0(config-if)#ip tcp adjust-mss 1360
iosv-0(config-if)#ip nhrp holdtime 450
iosv-0(config-if)#ip redirect
iosv-0(config-if)#no ip split-horizion eigrp 1
```

### Configure Spoke

After the hub is configured the spoke can be added to the mesh. There are a couple more NHRP commands here. First, the static mapping is necessary because it provides the overlay address of the Next Hop Server (NHS), and without that, none of the NHRP address mappings would be accessible.  The muticast command directly after that tells the spoke to send all multicast traffic to the hub. This allows for dynamic routing protocols to traverse the DMVPN. 

```
iosv-2(config)#interface tunnel 0
iosv-2(config-if)#bandwidth 1000
iosv-2(config-if)#ip address 10.0.0.12 255.255.255.0
iosv-2(config-if)#ip mtu 1400
iosv-2(config-if)#ip nhrp authentication Cisco123
iosv-2(config-if)#ip nhrp map 10.0.0.1 203.0.113.1
iosv-2(config-if)#ip nhrp map multicast 203.0.113.1
iosv-2(config-if)#ip nhrp network-id 100
iosv-2(config-if)#ip nhrp holdtime 450
iosv-2(config-if)#ip nhrp nhs 10.0.0.1
iosv-2(config-if)#ip nhrp shortcut
iosv-2(config-if)#no ip nhrp redirect
iosv-2(config-if)#ip tcp adjust-mss 1360
iosv-2(config-if)#tunnel source g0/0
iosv-2(config-if)#tunnel mode gre multipoint
iosv-2(config-if)#tunnel protection ipsec profile ipsec-profile
iosv-2(config-if)#
```

### Configure EIGRP

Finally, a standard EIGRP config is set up. The 192 network is the protected network that is to be allowed over the DMVPN. 

```
iosv-3(config)#router eigrp 1
iosv-3(config-router)#network 192.168.3.0 0.0.0.255
iosv-3(config-router)#network 10.0.0.0 0.0.0.255
iosv-3(config-router)#
```

### Verify

Below are some show commands that can verify that the DMVPN is correctly set up.

#### show dmvpn

This command shows the basic DMVPN information. The most important things of note are the three peers, and that each is dynamic indicated by “D” 

```
iosv-0#show dmvpn
Legend: Attrb --> S - Static, D - Dynamic, I - Incomplete
        N - NATed, L - Local, X - No Socket
        T1 - Route Installed, T2 - Nexthop-override
        C - CTS Capable, I2 - Temporary
        # Ent --> Number of NHRP entries with same NBMA peer
        NHS Status: E --> Expecting Replies, R --> Responding, W --> Waiting
        UpDn Time --> Up or Down Time for a Tunnel
==========================================================================

Interface: Tunnel0, IPv4 NHRP Details 
Type:Hub, NHRP Peers:3, 

 # Ent  Peer NBMA Addr Peer Tunnel Add State  UpDn Tm Attrb
 ----- --------------- --------------- ----- -------- -----
     1 203.0.113.11          10.0.0.11    UP 00:31:47     D
     1 203.0.113.12          10.0.0.12    UP 00:31:31     D
     1 203.0.113.13          10.0.0.13    UP 00:32:16     D

iosv-0#
```

#### show ip nhrp brief

This shows the NHRP mappings on the host.The overlay is on the left, and the underlay is on the right. Finally, the D/r indicates a dynamic mapping that is registered. 

```
iosv-0#show ip nhrp brief 
****************************************************************************
    NOTE: Link-Local, No-socket and Incomplete entries are not displayed
****************************************************************************
Legend: Type --> S - Static, D - Dynamic
        Flags --> u - unique, r - registered, e - temporary, c - claimed
        a - authoritative, t - route
============================================================================

Intf     NextHop Address                                    NBMA Address
         Target Network                              T/Flag
-------- ------------------------------------------- ------ ----------------
Tu0      10.0.0.11                                          203.0.113.11
         10.0.0.11/32                                D/r   
Tu0      10.0.0.12                                          203.0.113.12
         10.0.0.12/32                                D/r   
Tu0      10.0.0.13                                          203.0.113.13
         10.0.0.13/32                                D/r   
iosv-0#
```

#### Phase 3

```
iosv-2#traceroute 192.168.1.1
Type escape sequence to abort.
Tracing the route to 192.168.1.1
VRF info: (vrf in name/id, vrf out name/id)
  1 10.0.0.1 54 msec
  2 10.0.0.11 95 msec 45 msec * 
iosv-2#traceroute 192.168.1.1
Type escape sequence to abort.
Tracing the route to 192.168.1.1
VRF info: (vrf in name/id, vrf out name/id)
  1 10.0.0.11 69 msec 47 msec * 
iosv-2#
```