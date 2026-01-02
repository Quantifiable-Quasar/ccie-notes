---
layout: default
title: Site-to-Site VPNs
parent: Labs
---
# Site-to-Site VPNs
## Overview

The goal of this lab is be as comprehensive as possible to learn about Site-to-Site VPNs. It starts with a basic Crypto Map IKEv1 tunnel and evolves into a FlexVPN deployment.  The prerequisite labs should all be in <a class="reference-link" href="#root/y4v6Qzszu7ju/gJlWD4vacXMB">Todo</a>. 

<figure class="image image-style-align-center"><img style="aspect-ratio:624/309;" src="Site-to-Site VPNs_image.png" width="624" height="309"></figure>

1.  Infrastructure and Segmentation
    1.  Establish basic underlay connectivity
    2.  Dual Front Door VRF
    3.  Service Layer Segmentation
    4.  PKI
2.  Legacy IPsec
    1.  Hub-to-Branch 1 (Split HA)
    2.  Hub-to-Branch 2 (NAT-T)
    3.  Hub-to-Branch 3 (ASA)
3.  Dual Cloud DMVPN
    1.  Red VRF/BGP (Tunnel 100 and 200)
    2.  Blue/EIGRP (Tunnel 300 and 400)
    3.  ECMP for both VRFs
    4.  Branch 2 NHS clustering
    5.  ASA integration
4.  FlexVPN
    1.  Migrate everything to FlexVPN/IKEv2
    2.  Configure IKEv2 Load Balancing Cluster for hubs
    3.  Branch 2 client failover (FlexVPN client profile)
    4.  Branch 4 Hybrid ECMP (Dual Uplink)
    5.  ASA migration
    6.  SGT inline tagging
    7.  IPv6 dual stack