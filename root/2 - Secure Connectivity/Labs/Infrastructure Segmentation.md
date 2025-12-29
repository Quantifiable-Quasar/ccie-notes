---
layout: default
title: Infrastructure Segmentation
parent: Labs
---
# Infrastructure Segmentation
> [!NOTE]
> Note: Lab needs editing, currently completely Gemini generated

Based on the structure and format of the "Unified Ultimate Lab" document you provided<sup>111111111</sup>, I have designed a comprehensive lab outline tailored specifically to CCIE Security Exam Objectives 2.5 (Infrastructure Segmentation) and 2.6 (Microsegmentation with Cisco TrustSec).

<figure class="image"><img style="aspect-ratio:737/697;" src="Infrastructure Segmentatio.png" width="737" height="697"></figure>

<figure class="image"><img style="aspect-ratio:1127/622;" src="2_Infrastructure Segmentatio.png" width="1127" height="622"></figure>

Here is the complete, unified lab manual. It integrates the foundational segmentation tasks with the expert-level security overlays into a single, cohesive scenario.

* * *

# CCIE Security v6.1: The Segmentation & TrustSec Enforcement Lab

## 1\. Lab Strategy and Architectural Scope

This lab scenario simulates a "Zero Trust" retrofit of a legacy Enterprise Campus. You are moving from a flat Layer 2 network to a fully segmented, identity-aware architecture without replacing the underlying transport core.

**You are tasked with managing three distinct layers of isolation simultaneously:**

1.  **Macro-Segmentation:** Strict traffic isolation using Private VLANs (L2) and VRF-Lite (L3).
2.  **Micro-Segmentation:** Identity-based enforcement using Cisco TrustSec (SGT/SXP) and Zone-Based Firewalls.
3.  **Transport Security:** Overlay encryption using GETVPN and legacy GRE tunneling.

**Key Design Constraints:**

*   **Legacy Core:** The WAN Core is "untrusted" and does not support MPLS.
*   **Dual Tenancy:** "Corporate" and "Guest" traffic must never mix in the routing table, except for specific shared services.
*   **Identity First:** Policy must be enforced by User Role (SGT), not IP address.

* * *

## 2\. Master Topology Diagram

**Plate 1: The Zero Trust Overlay**

*   **Site A (Headquarters):** Includes DSW-1 (Core/Distribution), ASW-1 (Corp/IoT Access), and ASW-2 (Guest Access).
*   **Site B (Data Center):** Includes DSW-2 (Gateway) and Restricted Servers.
*   **Transport (WAN):** A simulated Legacy ISP Core providing only Global IP reachability.

* * *

## 3\. Phase 0: Layer 2 Isolation (VLAN & PVLAN)

**Goal:** Establish the foundation for local isolation at the Campus Access layer.

**3.1 Standard Segmentation**

*   **Objective 1:** On all Access Switches, create and name standard VLANs:
    *   VLAN 10: Engineering
    *   VLAN 20: HR/Finance
    *   VLAN 99: Management
*   **Objective 2:** Configure 802.1Q trunks between Access and Distribution layers. Prune unnecessary VLANs.

**3.2 Private VLANs (PVLANs) \[Exam Objective 2.5.b\]**

*   **Objective 1:** Configure a Primary VLAN (VLAN 500) for "IoT & Guest Devices."
*   **Objective 2:** Configure Secondary VLANs:
    *   **Community (501):** Guest Wi-Fi (Guests can communicate with other guests).
    *   **Isolated (502):** IoT Sensors (Strictly isolated; can only reach the gateway).
*   **Objective 3:** Associate the secondary VLANs to Primary VLAN 500.
*   **Objective 4:** Configure host ports in Promiscuous, Community, and Isolated modes.
*   **Objective 5:** Verify that an IoT sensor in VLAN 502 cannot ping another sensor in VLAN 502, but can reach the Promiscuous Gateway.

* * *

## 4\. Phase 1: Layer 3 Isolation (VRF-Lite)

**Goal:** Extend isolation up to the Core/Distribution layers ensuring "Corporate" and "Guest" routing tables never mix.

**4.1 VRF Definition \[Exam Objective 2.5.d\]**

*   **Objective 1:** On Distribution and Core routers, define two VRFs:
    *   **VRF\_CORP:** For Engineering and HR/Finance.
    *   **VRF\_GUEST:** For IoT and Guest traffic.
*   **Objective 2:** Migrate Layer 3 SVIs for VLAN 10/20 into `VRF_CORP` and VLAN 500 into `VRF_GUEST`.
*   **Objective 3:** Verify that a device in `VRF_CORP` cannot ping the gateway of `VRF_GUEST`.

**4.2 VRF-Aware Routing**

*   **Objective 1:** Configure OSPF Process 10 for `VRF_CORP` and OSPF Process 20 for `VRF_GUEST`.
*   **Objective 2:** Ensure routing updates for Corporate subnets are strictly contained within OSPF Process 10.

* * *

## 5\. Phase 2: Transport Overlay (GRE)

**Goal:** Bridge the segmented VRFs across a non-MPLS legacy core.

**5.1 GRE Infrastructure \[Exam Objective 2.5.c\]**

*   **Objective 1:** Create "Tunnel 10" to carry `VRF_CORP` traffic.
    *   Tunnel Source/Dest: Global WAN IPs.
    *   Tunnel VRF: `VRF_CORP`.
*   **Objective 2:** Create "Tunnel 20" to carry `VRF_GUEST` traffic.
    *   Tunnel Source/Dest: Global WAN IPs.
    *   Tunnel VRF: `VRF_GUEST`.
*   **Objective 3:** Establish OSPF adjacencies over both tunnels.
*   **Objective 4:** Verify Site A Engineering can reach Site B Engineering, but cannot reach Site B Guests.

* * *

## 6\. Phase 3: Microsegmentation (TrustSec & SXP)

**Goal:** Implement policy enforcement based on identity (SGT) rather than IP address.

**6.1 SGT Classification**

*   **Objective 1:** Enable TrustSec globally on Core/Distribution.
*   **Objective 2:** Define SGTs: 10 (Engineers), 20 (HR), 30 (Servers).
*   **Objective 3:** Configure **IP-to-SGT Static Mapping** on DSW-1 to classify the subnets.

**6.2 SXP Propagation \[Exam Objective 2.6\]**

*   **Objective 1:** Configure SXP between Access Switches (Speakers) and Distribution Switch (Listener) to simulate legacy access layer support.
*   **Objective 2:** Verify DSW-1 learns IP-to-SGT bindings via SXP.

**6.3 Enforcement (SGACL)**

*   **Objective 1:** Create an SGACL named "Protect-Servers."
    *   **SGT 10 (Eng) -> SGT 30 (Servers):** PERMIT
    *   **SGT 20 (HR) -> SGT 30 (Servers):** DENY
*   **Objective 2:** Apply the RBACL policy on the egress interface of the server segment.
*   **Objective 3:** Verify that HR traffic is dropped based on the SGT tag, despite having valid IP routing.

* * *

## 7\. Phase 4: Shared Services (Route Leaking)

**Goal:** Allow controlled access between VRFs for shared infrastructure.

**7.1 MP-BGP Route Leaking**

*   **Objective 1:** Configure a BGP Address Family for `VRF_CORP` and `VRF_GUEST`.
*   **Objective 2:** Create a "Shared DNS" Loopback (8.8.8.8) in `VRF_CORP`.
*   **Objective 3:** Use **Route Targets** to export the DNS route from Corp and import it into Guest.
*   **Objective 4:** Verify Guests can ping the DNS server but cannot reach any other Corp resources.

* * *

## 8\. Phase 5: Overlay Encryption (GETVPN)

**Goal:** Encrypt the GRE traffic traversing the untrusted Core using "Tunnel-less" VPN.

**8.1 Key Server (KS) & Group Member (GM)**

*   **Objective 1:** Configure DSW-1 as the GETVPN Key Server.
*   **Objective 2:** Define policy to encrypt **only** GRE traffic (Protocol 47) destined for Site B.
*   **Objective 3:** Configure DSW-1 and DSW-2 as Group Members.
*   **Objective 4:** Verify via packet capture that GRE packets are encapsulated in ESP (Protocol 50) on the physical wire, but the original IP headers remain visible (Tunnel-less mode).

* * *

## 9\. Phase 6: Identity-Aware Firewall (ZBFW)

**Goal:** Replace stateless SGACLs with Stateful Inspection using SGTs.

**9.1 Zone Configuration**

*   **Objective 1:** Create Security Zones: INSIDE, OUTSIDE, and VPN.
*   **Objective 2:** Assign physical interfaces and Tunnel interfaces to their respective zones.

**9.2 SGT-Based Policy**

*   **Objective 1:** Create ZBFW Class-Maps that match on **Source SGT**.
*   **Objective 2:** Create a Zone-Pair for **INSIDE-to-VPN**.
    *   **Policy:** Inspect traffic from SGT 10. Drop traffic from SGT 20.
*   **Objective 3:** Verify that GRE tunnel traffic is inspected statefully based on the user's SGT.

* * *

## 10\. Phase 7: IPv6 First-Hop Security

**Goal:** Secure the IPv6 Access Layer against rogue advertisements.

**10.1 Access Layer Hardening**

*   **Objective 1:** Configure **IPv6 RA Guard** on host-facing ports to block rogue Router Advertisements.
*   **Objective 2:** Configure **DHCPv6 Guard** to block unauthorized DHCPv6 server responses.
*   **Objective 3:** Enable **IPv6 Snooping** and **Source Guard** to validate source addresses against the binding table.

* * *

## 11\. Phase 8: Management Hardening

**Goal:** Secure the Control and Management planes.

**11.1 CoPP & MPP**

*   **Objective 1:** Configure **Control Plane Policing (CoPP)** to strictly rate-limit ICMP and SNMP to the CPU.
*   **Objective 2:** Configure **Management Plane Protection (MPP)** to allow SSH only from the Management VLAN (99)