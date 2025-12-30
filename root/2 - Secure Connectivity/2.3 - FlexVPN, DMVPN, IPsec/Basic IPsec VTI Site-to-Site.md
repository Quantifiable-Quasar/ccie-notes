---
layout: default
title: Basic IPsec VTI Site-to-Site
parent: 2.3 - FlexVPN, DMVPN, IPsec
---
# Basic IPsec VTI Site-to-Site
## Overview

The goal of this lab is to create the most basic IPsec site to site tunnel possible. This will serve as a “home base” for the other IPsec based configs and will be referenced by them. Below is the topology used and the high-level steps are listed.

<figure class="image"><img style="aspect-ratio:519/218;" src="1_Basic IPsec VTI Site-to-Si.png" width="519" height="218"></figure>

1.  Establish basic connectivity
2.  ikev2 proposal
3.  ikev2 policy
4.  ikev2 keyring
5.  ike profile
6.  ipsec profile
7.  vti

## Basic Connectivity

This should be obvious, but we need connectivity between the two routers so get that up

## IKEv2 Proposal/Policy

The proposal defines the phase 1 options that an endpoint can accept. Below three are chosen, but as long as the options meet the requirements noted in the output below they will work. 

```
R1(config)#crypto ikev2 proposal ike-prop
IKEv2 proposal MUST either have a set of an encryption algorithm other than aes-gcm, an integrity algorithm and a DH group configured or 
 encryption algorithm aes-gcm, a prf algorithm and a DH group configured
R1(config-ikev2-proposal)#encryption aes-gcm-256
R1(config-ikev2-proposal)#prf sha256
R1(config-ikev2-proposal)#group 14
R1(config-ikev2-proposal)#exit
R1(config)#crypto ikev2 policy ike-pol
IKEv2 policy MUST have atleast one complete proposal attached 
R1(config-ikev2-policy)#proposal ike-prop
R1(config-ikev2-policy)#
```

## IKEv2 Keyring

The keyring defines the authentication method and secret. The output below is using the most simple pre-shared key.

```
R1(config)#crypto ikev2 keyring ike-keyring
R1(config-ikev2-keyring)#peer R2
R1(config-ikev2-keyring-peer)#address 203.0.113.2
R1(config-ikev2-keyring-peer)#pre-shared-key Cisco123
R1(config-ikev2-keyring-peer)#
```

## IKE Profile

The profile ties everything together by defining the peers and authentication (using the selected keyring).

```
R1(config)#crypto ikev2 profile ike-profile
IKEv2 profile MUST have:
   1. A local and a remote authentication method.
   2. A match identity or a match certificate or match any statement.
R1(config-ikev2-profile)#match identity remote address 203.0.113.2
R1(config-ikev2-profile)#identity local address 203.0.113.1
R1(config-ikev2-profile)#authentication remote pre-share
R1(config-ikev2-profile)#authentication local pre-share
R1(config-ikev2-profile)#keyring local ike-keyring
R1(config-ikev2-profile)#    
```

## IPsec Profile

The IPsec profile defines phase 2 connection parameters. It includes the phase 1 IKE profile and the transform set. The transform set includes the cryptographic functions that can be used for phase 2. 

```
R1(config)#crypto ipsec transform-set ipsec-transform esp-gcm 256
R1(cfg-crypto-trans)#exit
R1(config)#crypto ipsec profile ipsec-profile
R1(ipsec-profile)#set transform-set ipsec-transform
R1(ipsec-profile)#set ikev2-profile ike-profile
R1(ipsec-profile)#exit
R1(config)#
```

## VTI

The Virtual Tunnel Interface (VTI) is an interface used for the overlay network created by the VPN. It uses a unique network, and the source/destination is explicitly defined. Here, the IPsec profile is linked. Finally, a static route is created to direct traffic to the protected network over the VPN. Dynamic protocols can be used, but this is the simplest way so that's what was used. 

```
R1(config)#interface Tunnel0
R1(config-if)#ip address 10.0.1.1 255.255.255.252
R1(config-if)#tunnel source e0/0
R1(config-if)#tunnel destination 203.0.113.2
R1(config-if)#tunnel protection ipsec profile ipsec-profile
R1(config-if)#exit
R1(config)#ip route 192.168.2.0 255.255.255.0 Tunnel0
R1(config)#
```

## Verify

Below are two show commands that can be useful. In the IKEv2 SA, look for READY as the staus. In the IPsec SA, look for ACTIVE as the status

```
R1#show crypto ikev2 sa
 IPv4 Crypto IKEv2  SA 

Tunnel-id Local                 Remote                fvrf/ivrf            Status 
1         203.0.113.1/500       203.0.113.2/500       none/none            READY  
      Encr: AES-GCM, keysize: 256, PRF: SHA256, Hash: None, DH Grp:14, Auth sign: PSK, Auth verify: PSK
      Life/Active Time: 86400/103 sec
      CE id: 1001, Session-id: 1
      Local spi: FD1996D514AA8EF0       Remote spi: 629C526363474999

 IPv6 Crypto IKEv2  SA 

R1#show crypto ipsec sa

interface: Tunnel0
    Crypto map tag: Tunnel0-head-0, local addr 203.0.113.1

   protected vrf: (none)
   local  ident (addr/mask/prot/port): (203.0.113.1/255.255.255.255/47/0)
   remote ident (addr/mask/prot/port): (203.0.113.2/255.255.255.255/47/0)
   current_peer 203.0.113.2 port 500
     PERMIT, flags={origin_is_acl,}
    #pkts encaps: 0, #pkts encrypt: 0, #pkts digest: 0
    #pkts decaps: 0, #pkts decrypt: 0, #pkts verify: 0
    #pkts compressed: 0, #pkts decompressed: 0
    #pkts not compressed: 0, #pkts compr. failed: 0
    #pkts not decompressed: 0, #pkts decompress failed: 0
    #send errors 0, #recv errors 0

     local crypto endpt.: 203.0.113.1, remote crypto endpt.: 203.0.113.2
     plaintext mtu 1446, path mtu 1500, ip mtu 1500, ip mtu idb Ethernet0/0
     current outbound spi: 0xFFCCC917(4291610903)
     PFS (Y/N): N, DH group: none

     inbound esp sas:
      spi: 0x53ABB47(87735111)
        transform: esp-gcm 256 ,
        in use settings ={Tunnel, }
        conn id: 1, flow_id: 1, sibling_flags FFFFFFFF80000040, crypto map: Tunnel0-head-0, initiator : False
         sa timing: remaining key lifetime (k/sec): (4334421/3449)
        IV size: 8 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)

     inbound ah sas:

     inbound pcp sas:

     outbound esp sas:
      spi: 0xFFCCC917(4291610903)
        transform: esp-gcm 256 ,
        in use settings ={Tunnel, }
        conn id: 2, flow_id: 2, sibling_flags FFFFFFFF80000040, crypto map: Tunnel0-head-0, initiator : False
         sa timing: remaining key lifetime (k/sec): (4334421/3449)
        IV size: 8 bytes
        replay detection support: Y
        Status: ACTIVE(ACTIVE)
          
     outbound ah sas:

     outbound pcp sas:
R1# 
```

This is what a packet capture looks like for that encrypted traffic. The ESP stuff is what's going over the VPN.

<figure class="image"><img style="aspect-ratio:1624/422;" src="Basic IPsec VTI Site-to-Si.png" width="1624" height="422"></figure>