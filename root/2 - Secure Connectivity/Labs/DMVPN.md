---
layout: default
title: DMVPN
parent: Labs
---
# DMVPN 
## Overview

The objective of this lab is to configure DMVPN. First, the configs are pretty much copied and pasted from [Cisco Docs](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/15-mt/sec-conn-dmvpn-15-mt-book/sec-conn-dmvpn-dmvpn.html). Below are the objectives that modify this configuration to achieve additional objectives. 

<figure class="image"><img style="aspect-ratio:420/479;" src="1_DMVPN_image.png" width="420" height="479"></figure>

1.  Configure basic DMVPN with spoke-to-spoke communication with Hub1
2.  Implement iBGP on cloud
3.  Create link between INET A and B and create dual-hub single cloud
4.  Delete link and create dual-hub multi cloud
5.  Migrate to IKEv2
6.  Implement PKI with CA being Hub
7.  Configure IPv6 on everything to dual stack network