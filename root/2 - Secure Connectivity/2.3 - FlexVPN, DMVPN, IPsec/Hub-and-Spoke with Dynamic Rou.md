---
layout: default
title: Hub-and-Spoke with Dynamic Rou
parent: 2.3 - FlexVPN, DMVPN, IPsec
---
# Hub-and-Spoke with Dynamic Routing
## Overview

This lab is a hub-and-spoke pure ipsec implementation with eigrp as the routing protocol. I'm not rewriting all the ipsec stuff so reference <a class="reference-link" href="Basic%20IPsec%20VTI%20Site-to-Site.md">Basic IPsec site-to-site</a> for those explicit instructions.

<figure class="image"><img style="aspect-ratio:950/384;" src="Hub-and-Spoke with Dynamic.png" width="950" height="384"></figure>

**Steps:**

1.  Basic Connectivity
2.  IPsec
3.  VTI
4.  EIGRP
5.  Adding a new spoke
6.  Verify

## IPsec 

### Hub

The keyring and policy are going to look a little different in this scenario. For the keyring, every peer needs to be defined, so now there are three entries. For the IKE profile, the match had to be wildcarded because now there are multiple peers. 

```
Hub-RTR(config)#crypto ikev2 keyring ike-key
Hub-RTR(config-ikev2-keyring)#peer spoke1
Hub-RTR(config-ikev2-keyring-peer)#address 192.0.2.2
Hub-RTR(config-ikev2-keyring-peer)#pre-shared-key Cisco123
Hub-RTR(config-ikev2-keyring-peer)#peer spoke2
Hub-RTR(config-ikev2-keyring-peer)#address 198.51.100.2
Hub-RTR(config-ikev2-keyring-peer)#pre-shared-key Cisco123
Hub-RTR(config-ikev2-keyring-peer)#peer spoke3
Hub-RTR(config-ikev2-keyring-peer)#address 203.0.113.2
Hub-RTR(config-ikev2-keyring-peer)#pre-shared-key Cisco123
Hub-RTR(config-ikev2-keyring-peer)#exit
Hub-RTR(config-ikev2-keyring)#exit
Hub-RTR(config)#crypto ikev2 profile ike-prof
IKEv2 profile MUST have:
   1. A local and a remote authentication method.
   2. A match identity or a match certificate or match any statement.
Hub-RTR(config-ikev2-profile)#match identity remote any
Hub-RTR(config-ikev2-profile)#authentication remote pre-share 
Hub-RTR(config-ikev2-profile)#authentication local pre-share 
Hub-RTR(config-ikev2-profile)#keyring local ike-key
Hub-RTR(config-ikev2-profile)#
```

### Spoke

This configuration example is from spoke3 which is iol-3 on the topology above. This is a basic site-to-site ipsec config, so it's pretty straightforward. 

```
R3(config)#crypto ikev2 proposal ike-prop 
R3(config-ikev2-proposal)# encryption aes-gcm-256
R3(config-ikev2-proposal)# prf sha256
R3(config-ikev2-proposal)# group 14
R3(config-ikev2-proposal)#crypto ikev2 policy ike-pol 
R3(config-ikev2-policy)# proposal ike-prop
R3(config-ikev2-policy)#crypto ikev2 keyring ike-key
R3(config-ikev2-keyring)# peer hub
R3(config-ikev2-keyring-peer)#address 203.0.113.1
R3(config-ikev2-keyring-peer)#pre-shared-key Cisco123
R3(config-ikev2-keyring-peer)#crypto ikev2 profile ike-prof
R3(config-ikev2-profile)#match identitity remote address 203.0.113.1 255.255.255.255    
R3(config-ikev2-profile)# authentication remote pre-share
R3(config-ikev2-profile)# authentication local pre-share
R3(config-ikev2-profile)# keyring local ike-key
R3(config-ikev2-profile)#crypto ipsec transform-set ike-tform esp-gcm 256 
R3(cfg-crypto-trans)# mode tunnel
R3(cfg-crypto-trans)#crypto ipsec profile ipsec-prof
R3(ipsec-profile)# set transform-set ike-tform 
R3(ipsec-profile)# set ikev2-profile ike-prof
R3(ipsec-profile)#exit
R3(config)#
```

## VTI

In this scenario, the VTIs on the client work the exact same as the normal site-to-site ipsec. On the hub, we need a new VTI for each tunnel that is to be created. Because these are interfaces, they need to be on separate networks, hence the /30s. 

### Hub

```
interface Tunnel1
 ip address 10.0.0.1 255.255.255.252
 tunnel source Ethernet0/1
 tunnel destination 192.0.2.2
 tunnel protection ipsec profile ipsec-prof
!
interface Tunnel2
 ip address 10.0.0.5 255.255.255.252
 tunnel source Ethernet0/2
 tunnel destination 198.51.100.2
 tunnel protection ipsec profile ipsec-prof
!
interface Tunnel3
 ip address 10.0.0.9 255.255.255.252
 tunnel source Ethernet0/3
 tunnel destination 203.0.113.2
 tunnel protection ipsec profile ipsec-prof
!
```

### Spoke

```
interface Tunnel0
 ip address 10.0.0.10 255.255.255.252
 tunnel source Ethernet0/0
 tunnel destination 203.0.113.1
 tunnel protection ipsec profile ipsec-prof
end
```

## EIGRP

Here, only the basic EIGRP configs need to be on each device. This is the EIGRP on the hub, so the advertised networks are the /30s attached to the VTIs. On the spoke routers, just add all the connected routes to be advertised. 

```
Hub-RTR(config)#router eigrp 100
Hub-RTR(config-router)#network 10.0.0.0 0.0.0.3
Hub-RTR(config-router)#network 10.0.0.4 0.0.0.3
Hub-RTR(config-router)#network 10.0.0.8 0.0.0.3
```

## Add a new spoke

Adding a new spoke is pretty easy. On the hub some basic configs need to be added, and the spoke obviously needs to be configured from scratch. Below is an example of adding a new spoke to the existing topology.

### Hub

The configs on the hub are simply the addition of the new interface, adding the peer to the keyring, creating a new VTI, and adding the new network to the EIGRP ASN.

```
Hub-RTR(config)#int e0/0
Hub-RTR(config-if)#no shut
Hub-RTR(config-if)#ip addr 128.210.211.1 255.255.255.0
Hub-RTR(config-if)#no shut
Hub-RTR(config-if)#exit
Hub-RTR(config)#crypto ikev2 keyring ike-key
Hub-RTR(config-ikev2-keyring)#peer spoke4
Hub-RTR(config-ikev2-keyring-peer)#address 128.210.211.2 255.255.255.0
Hub-RTR(config-ikev2-keyring-peer)#pre-shared-key Cisco123
Hub-RTR(config-ikev2-keyring-peer)#exit
Hub-RTR(config-ikev2-keyring)#exit
Hub-RTR(config)#interface Tunnel4
Hub-RTR(config-if)#ip address 10.0.0.13 255.255.255.252
Hub-RTR(config-if)#tunnel source e0/0
Hub-RTR(config-if)#tunnel destination 128.210.211.2p
Hub-RTR(config-if)#tunnel protection ipsec profile ipsec-prof
Hub-RTR(config-if)#exit        
Hub-RTR(config)#router eigrp 100
Hub-RTR(config-router)#network 10.0.0.12 0.0.0.3
```

### Spoke

These are the complete configs to add the spoke to the network. This should be achievable through the steps above, but they are here for reference. 

```
R4(config)#int e0/0
R4(config-if)#ip addr 128.210.211.2 255.255.255.0
R4(config-if)#no shut
R4(config-if)#exit
R4(config)#crypto ikev2 proposal ike-prop
IKEv2 proposal MUST either have a set of an encryption algorithm other than aes-gcm, an integrity algorithm and a DH group configured or 
 encryption algorithm aes-gcm, a prf algorithm and a DH group configured
R4(config-ikev2-proposal)#encryption aes-gcm-256
R4(config-ikev2-proposal)#prf sha256
R4(config-ikev2-proposal)#group 14
R4(config-ikev2-proposal)#exit
R4(config)#crypto ikev2 policy ike-pol
IKEv2 policy MUST have atleast one complete proposal attached 
R4(config-ikev2-policy)#proposal ike-prop
R4(config-ikev2-policy)#exit
R4(config)#crypto ikev2 keyring ike-key
R4(config-ikev2-keyring)#peer hub
R4(config-ikev2-keyring-peer)#address 128.210.211.1
R4(config-ikev2-keyring-peer)#pre-shared-key Cisco123
R4(config-ikev2-keyring-peer)#exit
R4(config-ikev2-keyring)#exit
R4(config)#crypto ikev2 profile ike-prof
IKEv2 profile MUST have:
   1. A local and a remote authentication method.
   2. A match identity or a match certificate or match any statement.
R4(config-ikev2-profile)#authentication local pre-share 
R4(config-ikev2-profile)#authentication remote pre-share
R4(config-ikev2-profile)#keyring local ike-key
R4(config-ikev2-profile)#match identity remote address 128.210.211.1
R4(config-ikev2-profile)#exit
R4(config)#crypto ipsec transform-set ipsec-tform esp-gcm 256
R4(cfg-crypto-trans)#exit
R4(config)#crypto ipsec profile ipsec-prof
R4(ipsec-profile)#set transform-set ipsec-tform         
R4(ipsec-profile)#set ikev2-profile ike-prof
R4(ipsec-profile)#exit
R4(config)#int tunnel0
R4(config-if)#ip addr 10.0.0.13 255.255.255.252
R4(config-if)#tunnel source e0/0
R4(config-if)#tunnel destination 128.210.211.1
R4(config-if)#tunnel protection ipsec profile ipsec-prof  
R4(config-if)#exit
R4(config)#router eigrp 100
R4(config-router)#network 10.0.0.12 0.0.0.3 
R4(config-router)#network 192.168.4.0 0.0.0.255  
R4(config-router)#end
R4#
```

## Verify

All this stuff is basic ipsec troubleshooting. EIGRP is in here too, but this should be pretty easy.

```
R3#show crypto ikev2 sa 
 IPv4 Crypto IKEv2  SA 

Tunnel-id Local                 Remote                fvrf/ivrf            Status 
3         203.0.113.2/500       203.0.113.1/500       none/none            READY  
      Encr: AES-GCM, keysize: 256, PRF: SHA256, Hash: None, DH Grp:14, Auth sign: PSK, Auth verify: PSK
      Life/Active Time: 86400/991 sec
      CE id: 1003, Session-id: 1
      Local spi: C2D69B854419BC7A       Remote spi: 4F5EDE7AD248770E

 IPv6 Crypto IKEv2  SA 

R3#
```

```
R3#show crypto ipsec sa

interface: Tunnel0
    Crypto map tag: Tunnel0-head-0, local addr 203.0.113.2

   protected vrf: (none)
   local  ident (addr/mask/prot/port): (203.0.113.2/255.255.255.255/47/0)
   remote ident (addr/mask/prot/port): (203.0.113.1/255.255.255.255/47/0)
   current_peer 203.0.113.1 port 500
     PERMIT, flags={origin_is_acl,}
    #pkts encaps: 230, #pkts encrypt: 230, #pkts digest: 230
    #pkts decaps: 230, #pkts decrypt: 230, #pkts verify: 230
    #pkts compressed: 0, #pkts decompressed: 0
    #pkts not compressed: 0, #pkts compr. failed: 0
    #pkts not decompressed: 0, #pkts decompress failed: 0
    #send errors 0, #recv errors 0

     local crypto endpt.: 203.0.113.2, remote crypto endpt.: 203.0.113.1
     plaintext mtu 1446, path mtu 1500, ip mtu 1500, ip mtu idb Ethernet0/0
     current outbound spi: 0x2C042D64(738471268)
     PFS (Y/N): N, DH group: none

     inbound esp sas:
      spi: 0x15AF1474(363795572)
        transform: esp-gcm 256 ,
        in use settings ={Tunnel, }
        conn id: 6, flow_id: 6, sibling_flags FFFFFFFF80004040, crypto map: Tunnel0-head-0, initiator : True
         sa timing: remaining key lifetime (k/sec): (4259661/2577)
        IV size: 8 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)

     inbound ah sas:

     inbound pcp sas:

     outbound esp sas:
      spi: 0x2C042D64(738471268)
        transform: esp-gcm 256 ,
        in use settings ={Tunnel, }
        conn id: 5, flow_id: 5, sibling_flags FFFFFFFF80004040, crypto map: Tunnel0-head-0, initiator : True
         sa timing: remaining key lifetime (k/sec): (4259661/2577)
        IV size: 8 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)
          
     outbound ah sas:

     outbound pcp sas:
R3#
```

```
R3#show ip eigrp neighbors 
EIGRP-IPv4 Neighbors for AS(100)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
0   10.0.0.9                Tu0                      13 00:17:26    4  1470  0  32
R3#show ip eigrp topology 
EIGRP-IPv4 Topology Table for AS(100)/ID(1.1.1.1)
Codes: P - Passive, A - Active, U - Update, Q - Query, R - Reply,
       r - reply Status, s - sia Status 

P 192.168.3.0/24, 1 successors, FD is 281600
        via Connected, Ethernet0/1
P 10.0.0.12/30, 1 successors, FD is 28160000
        via 10.0.0.9 (28160000/26880000), Tunnel0
P 192.168.2.0/24, 1 successors, FD is 28185600
        via 10.0.0.9 (28185600/26905600), Tunnel0
P 10.0.0.8/30, 1 successors, FD is 26880000
        via Connected, Tunnel0
P 10.0.0.0/30, 1 successors, FD is 28160000
        via 10.0.0.9 (28160000/26880000), Tunnel0
P 192.168.1.0/24, 1 successors, FD is 28185600
        via 10.0.0.9 (28185600/26905600), Tunnel0
P 10.0.0.4/30, 1 successors, FD is 28160000
        via 10.0.0.9 (28160000/26880000), Tunnel0

R3#
```