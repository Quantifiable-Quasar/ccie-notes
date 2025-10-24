---
layout: default
title: Labs
---

# Labs
## IPsec

## Crypto robustness

*   Perfect Forward Secrecy: enable PFS on child SAs and validate that rekeys perform a fresh DH exchange; record CPU/latency impact and failure behavior when peers mismatch PFS groups.
*   ​
*   Rekey strategy: tune IKE and IPsec lifetimes asymmetrically (e.g., 10–20% offset) and observe SA overlap vs. flap during rekey on VTIs and crypto‑maps.
*   ​
*   DPD/liveness: configure Dead Peer Detection and confirm failover/cleanup timing when a peer disappears or a NAT state times out.
    *   ​

## MTU and fragmentation

*   Overhead tuning: validate ip mtu 1400 and ip tcp adjust‑mss 1360 for GRE+IPsec or VTI scenarios, and watch for drops when DF is set; compare transport vs. tunnel mode overhead.
*   ​
*   Troubleshoot path MTU: generate large pings with DF and confirm PMTUD behavior across the encrypted path; capture before/after adjustments.
    *   ​

## QoS and classification

*   Per‑tunnel QoS: classify/mark on the tunnel vs. WAN and test qos pre‑classify only when matching on 5‑tuple; document differences when classifying by DSCP only.
*   ​
*   Voice/critical data experiment: send EF/AF traffic mixes and verify policing/shaping counters on the tunnel and physical interfaces.
    *   ​

## Identity and keying variations

*   IKEv2 identity matching: switch between address, FQDN, and cert‑based identities; induce a mismatch to practice debug and profile selection.
*   ​
*   PKI lifecycle: test CRL/OCSP unreachability, cert expiration, and revocation to see negotiation failure modes with RSA‑sig tunnels.
    *   ​

## NAT and selectors

*   NAT‑T edge cases: shorten UDP/4500 idle timers on the NAT device, then generate periodic keepalives or traffic to keep SAs alive; verify behavior when public IP changes.
*   ​
*   Proxy‑ID/ACL overlap: deliberately create asymmetric or overlapping “interesting” ACLs and fix them; note how ASA proxy‑ID strictness differs from IOS.

## Routing behavior over IPsec

*   EIGRP features over VTI: try stub, summarization, unequal‑cost (variance), and route filtering; observe how selectorless VTIs keep SAs up while routes churn.
*   ​
*   Fail path scenarios: flap WAN on a spoke and compare convergence and SA churn between crypto‑map and VTI approaches.
    *   ​

## Observability and runbooks

*   Instrumentation: standardize a verification checklist per scenario using show crypto ikev2 sa, show crypto ipsec sa, platform packet‑tracer (ASA), and interface drops/MTU stats; keep before/after captures for rekey and MTU tests.
*   ​
*   Event timing: measure first‑packet delay for new SAs vs. warm SAs, and document expected bring‑up and rekey timings for each configuration

## DMVPN

*   Here are concise, five‑router lab outlines for each advanced DMVPN scenario, with goals, topology, key configs, and verification steps that fit the CML Free node limit.[thisbridgeistheroot](https://thisbridgeistheroot.com/blog/dmvpn-deep-dive-nhrp-mgre-routing-scenarios)​
    
    ### Dual‑hub single‑cloud
    
    *   Goal: Add a second hub for resiliency and let spokes register to both hubs while keeping a single NBMA cloud.[networklessons](https://networklessons.com/cisco/ccie-enterprise-infrastructure/dmvpn-dual-hub-single-cloud)​
    *   Topology: Hub1, Hub2, SpokeA, SpokeB, SpokeC on one shared “Internet” switch; Phase 3 with Hub1 primary.[networklessons](https://networklessons.com/cisco/ccie-enterprise-infrastructure/dmvpn-dual-hub-single-cloud)​
    *   Key configs: Spokes register to both hubs (ip nhrp nhs hub1 and hub2), hubs use ip nhrp map multicast dynamic, and Phase 3 with ip nhrp redirect on both hubs and ip nhrp shortcut on spokes; keep one tunnel per router.[journey2theccie.wordpress+1](https://journey2theccie.wordpress.com/2020/04/17/dmvpn-phase-3-configuration/)​
    *   Tests: Shut Tunnel on Hub1 to force failover, verify NHRP entries and routing remain intact with show dmvpn, show ip nhrp, and traceroute between spoke LANs.[networklessons](https://networklessons.com/cisco/ccie-enterprise-infrastructure/dmvpn-dual-hub-single-cloud)​
    
    ## Dual‑hub dual‑cloud
    
    *   Goal: Split the overlay across two independent DMVPN clouds for higher resiliency and path selection.[networklessons](https://networklessons.com/vpn/dmvpn-dual-hub-dual-cloud)​
    *   Topology: Hub1 terminates Cloud‑A, Hub2 terminates Cloud‑B, each spoke has Tunnel0 to Hub1 and Tunnel1 to Hub2 using two NBMA switches; reuse 5 routers by having three spokes multi‑home.[networklessons](https://networklessons.com/vpn/dmvpn-dual-hub-dual-cloud)​
    *   Key configs: Unique tunnel keys per cloud, matching ip nhrp network‑id per cloud, and separate routing instances or metrics to prefer Cloud‑A with controlled fallback to Cloud‑B.[journey2theccie.wordpress+1](https://journey2theccie.wordpress.com/2020/04/24/dmvpn-dual-hub-dual-cloud/)​
    *   Tests: Pull an “ISP” link for Cloud‑A and confirm spokes retain reachability via Cloud‑B with EIGRP/OSPF/BGP swaps and NHRP entries per cloud.[networklessons](https://networklessons.com/vpn/dmvpn-dual-hub-dual-cloud)​
    
    ## Hierarchical DMVPN
    
    *   Goal: Use a regional hub that aggregates spokes and uplinks to a core hub to localize traffic and scaling.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/211292-Configure-Phase-3-Hierarchical-DMVPN-wit.html)​
    *   Topology: CoreHub, RegionalHub, SpokeA, SpokeB, SpokeC on one or two NBMA clouds depending on space; spokes register to RegionalHub, which also forms as a spoke to CoreHub.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/211292-Configure-Phase-3-Hierarchical-DMVPN-wit.html)​
    *   Key configs: Phase 3 on both hub layers, summarization at RegionalHub toward CoreHub, and ip nhrp redirect/shortcut end‑to‑end.[journey2theccie.wordpress+1](https://journey2theccie.wordpress.com/2020/04/17/dmvpn-phase-3-configuration/)​
    *   Tests: Inter‑spoke traffic within the region should become spoke‑to‑spoke, while cross‑region uses CoreHub path with correct shortcuts and summaries.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/211292-Configure-Phase-3-Hierarchical-DMVPN-wit.html)​
    
    ## BGP over Phase 3
    
    *   Goal: Run BGP across DMVPN and validate hub as route‑reflector vs eBGP designs.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/222585-configure-bgp-over-dmvpn-phase-3.html)​
    *   Topology: Hub as RR (or eBGP hub), four spokes as RR‑clients or eBGP neighbors using one DMVPN cloud.[networklessons](https://networklessons.com/vpn/dmvpn-phase-3-bgp-routing)​
    *   Key configs: For iBGP, make hub RR and spokes RR‑clients with next‑hop‑self or next‑hop‑unchanged as needed; for eBGP, use unique AS per spoke and control next‑hop and MED for spoke‑to‑spoke.[ipspace+1](https://blog.ipspace.net/2014/03/scaling-bgp-based-dmvpn-networks/)​
    *   Tests: Confirm spoke‑to‑spoke prefixes install with correct next‑hop and NHRP shortcuts form without suboptimal hub data‑plane.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/222585-configure-bgp-over-dmvpn-phase-3.html)​
    
    ## IKEv2 with certificates
    
    *   Goal: Replace PSKs with PKI and RSA‑sig authentication for stronger identity and easier scale.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/224281-configure-dmvpn-phase-3-using-ikev2.html)​
    *   Topology: One hub, three spokes, plus use the hub or one router as local CA to stay within 5 routers.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/224281-configure-dmvpn-phase-3-using-ikev2.html)​
    *   Key configs: Enroll trustpoints on all routers, IKEv2 profile authentication remote rsa‑sig and local rsa‑sig with keyring removed, and tunnel protection referencing the IKEv2 profile.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/224281-configure-dmvpn-phase-3-using-ikev2.html)​
    *   Tests: show crypto ikev2 sa shows RSA‑sig auth, and revoking a cert on the CA prevents IKEv2 SA formation.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/224281-configure-dmvpn-phase-3-using-ikev2.html)​
    
    ## Per‑tunnel QoS
    
    *   Goal: Prioritize traffic on a per‑spoke basis using NHRP groups and per‑tunnel policies.[cisco](http://www.cisco.com/en/US/docs/ios-xml/ios/sec_conn_dmvpn/configuration/15-2mt/sec-conn-dmvpn-per-tunnel-qos.html)​
    *   Topology: One hub and four spokes on a single cloud, with each spoke assigned an NHRP group.[networklessons](https://networklessons.com/vpn/dmvpn-per-tunnel-qos)​
    *   Key configs: Apply tunnel‑mode per‑tunnel QoS with class‑maps/policy‑maps and qos pre‑classify on the tunnel to classify inner headers before encryption.[cisco+1](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/15-mt/sec-conn-dmvpn-15-mt-book/sec-conn-dmvpn-per-tunnel-qos.html)​
    *   Tests: Generate traffic classes from each spoke and verify shaping/drops per NHRP group with show policy‑map interface on tunnels.[networklessons](https://networklessons.com/vpn/dmvpn-per-tunnel-qos)​
    
    ## PfR/IWAN‑style path control
    
    *   Goal: Select paths based on performance across two transports while the routing remains steady.[ciscopress](https://www.ciscopress.com/articles/article.asp?p=2755712)​
    *   Topology: Two hubs (each on a different “ISP” switch) and three spokes with dual tunnels, reusing the dual‑cloud build.[cisco](http://www.cisco.com/en/US/docs/ios-xml/ios/pfr/configuration/15-2s/pfr-eigrp-mgre.html)​
    *   Key configs: Define PfR master and border roles, set policies for delay/loss/jitter, and allow dynamic path control between Cloud‑A and Cloud‑B for selected prefixes.[ciscopress+1](https://www.ciscopress.com/articles/article.asp?p=2755712)​
    *   Tests: Inject loss/latency on one cloud and confirm PfR moves flows to the better tunnel without routing reconvergence.[cisco](http://www.cisco.com/en/US/docs/ios-xml/ios/pfr/configuration/15-2s/pfr-eigrp-mgre.html)​
    
    ## IPv6 over DMVPN
    
    *   Goal: Carry IPv6 over IPv4 NBMA using DMVPN with OSPFv3 or BGP for overlay routing.[cisco](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/xe-16/sec-conn-dmvpn-xe-16-book/ip6-dmvpn-xe.html)​
    *   Topology: One hub and four spokes; tunnels use IPv6 addresses while WAN/NBMA stays IPv4.[networklessons](https://networklessons.com/cisco/ccie-routing-switching/dmvpn-ipv6-over-ipv4)​
    *   Key configs: Enable IPv6 on tunnels, run OSPFv3/BGP over the tunnel, and validate NHRP operation while encapsulating IPv6 in GRE/IPsec over IPv4.[cisco](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/xe-16/sec-conn-dmvpn-xe-16-book/ip6-dmvpn-xe.html)​
    *   Tests: Spoke‑to‑spoke IPv6 traffic forms shortcuts and survives hub failure if dual hubs are added later.[cisco](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/xe-16/sec-conn-dmvpn-xe-16-book/ip6-dmvpn-xe.html)​
    
    ## Front‑door VRF (fVRF)
    
    *   Goal: Separate underlay transport from overlay routing for multi‑tenant or split‑provider scenarios with IKEv2.[ccietbd](https://ccietbd.com/2023/03/18/study-notes-ikev2-dmvpn-with-rsa-sig-auth-and-fvrf/)​
    *   Topology: One hub and three spokes with an underlay fVRF for WAN and a global/overlay VRF for LAN, plus one extra spoke or hub for five routers total.[ccietbd](https://ccietbd.com/2023/03/18/study-notes-ikev2-dmvpn-with-rsa-sig-auth-and-fvrf/)​
    *   Key configs: Put WAN interfaces and IKEv2 keying in the fVRF, bind the tunnel source to the fVRF, and keep the overlay routing in the global or service VRF.[ccietbd](https://ccietbd.com/2023/03/18/study-notes-ikev2-dmvpn-with-rsa-sig-auth-and-fvrf/)​
    *   Tests: Verify that underlay reachability is VRF‑isolated while overlay subnets route end‑to‑end.[ccietbd](https://ccietbd.com/2023/03/18/study-notes-ikev2-dmvpn-with-rsa-sig-auth-and-fvrf/)​
    
    ## Multicast over DMVPN
    
    *   Goal: Enable multicast applications and routing protocols that rely on multicast across Phase 3.[cisco](https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-multicast/b-ip-multicast/m_sec-conn-dmvpn-dmvpn-0.html)​
    *   Topology: One hub as RP and three spokes using PIM sparse‑mode on Tunnel interfaces.[cisco](https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-multicast/b-ip-multicast/m_sec-conn-dmvpn-dmvpn-0.html)​
    *   Key configs: Enable PIM on tunnels and LANs, set RP at hub, ensure NHRP mappings allow multicast replication via ip nhrp map multicast dynamic.[cisco](https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-multicast/b-ip-multicast/m_sec-conn-dmvpn-dmvpn-0.html)​
    *   Tests: Multicast receivers on spokes join groups and receive streams across spoke‑to‑spoke shortcuts after initial control flows.[cisco](https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-multicast/b-ip-multicast/m_sec-conn-dmvpn-dmvpn-0.html)​
    
    ## Operational runbook lab
    
    *   Goal: Build a verification/troubleshooting playbook and practice break/fix for DMVPN, NHRP, and IPsec.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/111976-dmvpn-troubleshoot-00.html)​
    *   Topology: Any of the above five‑router setups; induce issues like NHRP auth mismatches, missing multicast maps, or MTU problems and recover.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/111976-dmvpn-troubleshoot-00.html)​
    *   Key steps: Use show dmvpn, show ip nhrp, show crypto ikev2/ipsec sa, and traceroute to isolate failures and measure bring‑up times and cache behavior.[cisco](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/111976-dmvpn-troubleshoot-00.html)​
    
    If helpful, each outline can be expanded into step‑by‑step configs tailored to the exact platforms in CML Free, including interface names and sample addressing that match your current lab.[thisbridgeistheroot](https://thisbridgeistheroot.com/blog/dmvpn-deep-dive-nhrp-mgre-routing-scenarios)​
*   Add to follow-up
    
    Check sources
*   [https://thisbridgeistheroot.com/blog/dmvpn-deep-dive-nhrp-mgre-routing-scenarios](https://thisbridgeistheroot.com/blog/dmvpn-deep-dive-nhrp-mgre-routing-scenarios)
*   [https://networklessons.com/cisco/ccie-enterprise-infrastructure/dmvpn-dual-hub-single-cloud](https://networklessons.com/cisco/ccie-enterprise-infrastructure/dmvpn-dual-hub-single-cloud)
*   [https://learningnetwork.cisco.com/s/article/cciev5-dmvpn-labs-workbook](https://learningnetwork.cisco.com/s/article/cciev5-dmvpn-labs-workbook)
*   [https://itexamanswers.net/19-1-3-lab-implement-a-dmvpn-phase-1-hub-to-spoke-topology-answers.html](https://itexamanswers.net/19-1-3-lab-implement-a-dmvpn-phase-1-hub-to-spoke-topology-answers.html)
*   [http://www.cisco.com/en/US/technologies/tk583/tk372/technologies\_white\_paper0900aecd802b8f3c.html](http://www.cisco.com/en/US/technologies/tk583/tk372/technologies_white_paper0900aecd802b8f3c.html)
*   [https://www.youtube.com/watch?v=ioy\_81c1ax8](https://www.youtube.com/watch?v=ioy_81c1ax8)
*   [https://www.networktut.com/dmvpn-tutorial](https://www.networktut.com/dmvpn-tutorial)
*   [https://journey2theccie.wordpress.com/2020/04/22/dmvpn-phase-3-bgp/](https://journey2theccie.wordpress.com/2020/04/22/dmvpn-phase-3-bgp/)
*   [https://networklessons.com/vpn/dmvpn-phase-1-ospf-routing](https://networklessons.com/vpn/dmvpn-phase-1-ospf-routing)
*   [https://journey2theccie.wordpress.com/2020/04/17/dmvpn-phase-3-configuration/](https://journey2theccie.wordpress.com/2020/04/17/dmvpn-phase-3-configuration/)
*   [https://networklessons.com/vpn/dmvpn-dual-hub-dual-cloud](https://networklessons.com/vpn/dmvpn-dual-hub-dual-cloud)
*   [https://journey2theccie.wordpress.com/2020/04/24/dmvpn-dual-hub-dual-cloud/](https://journey2theccie.wordpress.com/2020/04/24/dmvpn-dual-hub-dual-cloud/)
*   [https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/211292-Configure-Phase-3-Hierarchical-DMVPN-wit.html](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/211292-Configure-Phase-3-Hierarchical-DMVPN-wit.html)
*   [https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/222585-configure-bgp-over-dmvpn-phase-3.html](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/222585-configure-bgp-over-dmvpn-phase-3.html)
*   [https://networklessons.com/vpn/dmvpn-phase-3-bgp-routing](https://networklessons.com/vpn/dmvpn-phase-3-bgp-routing)
*   [https://blog.ipspace.net/2014/03/scaling-bgp-based-dmvpn-networks/](https://blog.ipspace.net/2014/03/scaling-bgp-based-dmvpn-networks/)
*   [https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/224281-configure-dmvpn-phase-3-using-ikev2.html](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/224281-configure-dmvpn-phase-3-using-ikev2.html)
*   [http://www.cisco.com/en/US/docs/ios-xml/ios/sec\_conn\_dmvpn/configuration/15-2mt/sec-conn-dmvpn-per-tunnel-qos.html](http://www.cisco.com/en/US/docs/ios-xml/ios/sec_conn_dmvpn/configuration/15-2mt/sec-conn-dmvpn-per-tunnel-qos.html)
*   [https://networklessons.com/vpn/dmvpn-per-tunnel-qos](https://networklessons.com/vpn/dmvpn-per-tunnel-qos)
*   [https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec\_conn\_dmvpn/configuration/15-mt/sec-conn-dmvpn-15-mt-book/sec-conn-dmvpn-per-tunnel-qos.html](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/15-mt/sec-conn-dmvpn-15-mt-book/sec-conn-dmvpn-per-tunnel-qos.html)
*   [https://www.ciscopress.com/articles/article.asp?p=2755712](https://www.ciscopress.com/articles/article.asp?p=2755712)
*   [http://www.cisco.com/en/US/docs/ios-xml/ios/pfr/configuration/15-2s/pfr-eigrp-mgre.html](http://www.cisco.com/en/US/docs/ios-xml/ios/pfr/configuration/15-2s/pfr-eigrp-mgre.html)
*   [https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec\_conn\_dmvpn/configuration/xe-16/sec-conn-dmvpn-xe-16-book/ip6-dmvpn-xe.html](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_conn_dmvpn/configuration/xe-16/sec-conn-dmvpn-xe-16-book/ip6-dmvpn-xe.html)
*   [https://networklessons.com/cisco/ccie-routing-switching/dmvpn-ipv6-over-ipv4](https://networklessons.com/cisco/ccie-routing-switching/dmvpn-ipv6-over-ipv4)
*   [https://ccietbd.com/2023/03/18/study-notes-ikev2-dmvpn-with-rsa-sig-auth-and-fvrf/](https://ccietbd.com/2023/03/18/study-notes-ikev2-dmvpn-with-rsa-sig-auth-and-fvrf/)
*   [https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-multicast/b-ip-multicast/m\_sec-conn-dmvpn-dmvpn-0.html](https://www.cisco.com/c/en/us/td/docs/routers/ios/config/17-x/ip-multicast/b-ip-multicast/m_sec-conn-dmvpn-dmvpn-0.html)
*   [https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/111976-dmvpn-troubleshoot-00.html](https://www.cisco.com/c/en/us/support/docs/security/dynamic-multipoint-vpn-dmvpn/111976-dmvpn-troubleshoot-00.html)