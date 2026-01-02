---
layout: default
title: Basic FlexVPN
parent: 2.3 - FlexVPN, DMVPN, IPsec
---
# Basic FlexVPN
## Overview

FlexVPN is the next evolution of this VPN thing.

basic ipsec crypto configs

```
iosv-1(config)#crypto ikev2 proposal FLEXVPN_PROPOSAL 
iosv-1(config-ikev2-proposal)# encryption aes-cbc-256
iosv-1(config-ikev2-proposal)# integrity sha256
iosv-1(config-ikev2-proposal)# group 14
iosv-1(config-ikev2-proposal)#crypto ikev2 policy FLEXVPN_POLICY 
iosv-1(config-ikev2-policy)# proposal FLEXVPN_PROPOSAL
% Policy already has same proposal set 
iosv-1(config-ikev2-policy)#crypto ikev2 keyring FLEXVPN_KEYRING
iosv-1(config-ikev2-keyring)# peer FLEVPNPeers
iosv-1(config-ikev2-keyring-peer)#  address 0.0.0.0 0.0.0.0
iosv-1(config-ikev2-keyring-peer)#  pre-shared-key local cisco123
iosv-1(config-ikev2-keyring-peer)#  pre-shared-key remote cisco123
iosv-1(config-ikev2-keyring-peer)# !
iosv-1(config-ikev2-keyring-peer)#crypto ikev2 profile FLEXVPN_PROFILE
IKEv2 profile MUST have:
   1. A local and a remote authentication method.
   2. A match identity or a match certificate or match any statement.
iosv-1(config-ikev2-profile)# match identity remote any
iosv-1(config-ikev2-profile)# authentication remote pre-share
iosv-1(config-ikev2-profile)# authentication local pre-share
iosv-1(config-ikev2-profile)# keyring local FLEXVPN_KEYRING
iosv-1(config-ikev2-profile)# virtual-template 1
iosv-1(config-ikev2-profile)#$m-set FLEXVPN_TSET esp-aes esp-sha256-hmac     
iosv-1(cfg-crypto-trans)# mode tunnel
iosv-1(cfg-crypto-trans)#crypto ipsec profile FLEXVPN_IPSEC_PROFILE
iosv-1(ipsec-profile)# set transform-set FLEXVPN_TSET 
iosv-1(ipsec-profile)# set ikev2-profile FLEXVPN_PROFILE
```