---
layout: default
title: resources
parent: 2.5 Infrastructure Segmentation Methods
---
# resources
## VLAN

##### Links

*   [https://www.youtube.com/watch?v=uXnILE7fvog&list=PLxbwE86jKRgOb2uny1CYEzyRy\_mc-lE39&index=27](https://www.youtube.com/watch?v=uXnILE7fvog&list=PLxbwE86jKRgOb2uny1CYEzyRy_mc-lE39&index=27)
*   [https://www.youtube.com/watch?v=Xk46nm9FIUQ&list=PLxbwE86jKRgOb2uny1CYEzyRy\_mc-lE39&index=28](https://www.youtube.com/watch?v=Xk46nm9FIUQ&list=PLxbwE86jKRgOb2uny1CYEzyRy_mc-lE39&index=28)
*   [https://www.youtube.com/watch?v=M7fFjFtN6jM&list=PLxbwE86jKRgOb2uny1CYEzyRy\_mc-lE39&index=29](https://www.youtube.com/watch?v=M7fFjFtN6jM&list=PLxbwE86jKRgOb2uny1CYEzyRy_mc-lE39&index=29)
*   [https://www.youtube.com/watch?v=o\_d4T7Ig9qA&list=PLxbwE86jKRgOb2uny1CYEzyRy\_mc-lE39&index=30](https://www.youtube.com/watch?v=o_d4T7Ig9qA&list=PLxbwE86jKRgOb2uny1CYEzyRy_mc-lE39&index=30)
*   [https://www.youtube.com/watch?v=SvmjnkthjeM&list=PLxbwE86jKRgOb2uny1CYEzyRy\_mc-lE39&index=31](https://www.youtube.com/watch?v=SvmjnkthjeM&list=PLxbwE86jKRgOb2uny1CYEzyRy_mc-lE39&index=31)
*   [https://www.youtube.com/watch?v=zAHe6D783fM&list=PLxbwE86jKRgOb2uny1CYEzyRy\_mc-lE39&index=32](https://www.youtube.com/watch?v=zAHe6D783fM&list=PLxbwE86jKRgOb2uny1CYEzyRy_mc-lE39&index=32)
*   [https://www.youtube.com/watch?v=YRyc\_5Oxds4&list=PLxyr0C\_3Ton1X7ex2fhxtjc6D1PPAumd2&index=34](https://www.youtube.com/watch?v=YRyc_5Oxds4&list=PLxyr0C_3Ton1X7ex2fhxtjc6D1PPAumd2&index=34)
*   [https://www.youtube.com/watch?v=6ow2RLdJj0U&list=PLxyr0C\_3Ton1X7ex2fhxtjc6D1PPAumd2&index=35](https://www.youtube.com/watch?v=6ow2RLdJj0U&list=PLxyr0C_3Ton1X7ex2fhxtjc6D1PPAumd2&index=35)
*   https://www.youtube.com/watch?v=6ow2RLdJj0U&list=PLxyr0C\_3Ton1X7ex2fhxtjc6D1PPAumd2&index=36

## PVLAN

*   [https://www.youtube.com/watch?v=FnVqZwM42tY](https://www.youtube.com/watch?v=FnVqZwM42tY)
*   https://www.youtube.com/watch?v=6ow2RLdJj0U&list=PLxyr0C\_3Ton1X7ex2fhxtjc6D1PPAumd2&index=37

## GRE

## VRF-Lite

You are absolutely right. VRF-Lite is a massive topic because it moves you from "Layer 2 separation" (VLANs) to "Layer 3 separation" (Virtual Routing Tables). In the CCIE exam, **VRF-Lite is almost always the answer** when the question asks for "complete isolation of routing tables" or "segmentation without MPLS."

Here is the breakdown of Use Cases and a progressive Lab Series to master it.

### **Common Use Cases (Why we do this)**

1.  **Mergers & Acquisitions:** Company A buys Company B. Both use `10.0.0.0/8`. You need to connect them to the same router without re-IPing the entire network immediately.
2.  **Guest vs. Corporate:** You want the Guest WiFi to hit the internet router but **never** have a route to the Internal Server subnet in the routing table.
3.  **Shared Services:** Multiple isolated departments (HR, Finance) need to access a single shared resource (like a DNS server or Internet Gateway) but shouldn't talk to each other.
4.  **Management Plane Protection:** Creating a `Mgmt-VRF` so that production data traffic can never "accidentally" route to the management ports.
5.  **Front Door VRF (FVRF):** Used in DMVPN/SD-WAN. The encrypted tunnel interface is in the "Inside" VRF, but the encrypted packets are transported out a physical interface in the "Outside" (Front Door) VRF.

* * *

### **The Lab Series**

We will move from basic syntax to complex route leaking.

#### **Phase 1: The Foundations (Modern Syntax)**

_Note: Cisco has two ways to do VRF._ `_ip vrf <name>_` _(Legacy) and_ `_vrf definition <name>_` _(Modern, supports IPv6). **Always study the modern syntax** for CCIE._

**1\. The Overlapping IP Proof**

*   **Objective:** Create `vrf definition RED` and `vrf definition BLUE`.
*   **Task:** Assign `192.168.1.1/24` to Loopback 1 (RED) and `192.168.1.1/24` to Loopback 2 (BLUE).
*   **Verify:** Prove they are unique by checking `show ip route vrf RED` vs `BLUE`.
*   **Gotcha:** Notice that when you apply `vrf forwarding <name>` to an interface, **Cisco deletes the IP address**. You must re-add the IP _after_ assigning the VRF.

**2\. VRF-Lite with OSPF (Process vs. Address Family)**

*   **Objective:** Peer with two different neighbors, one in RED, one in BLUE.
*   **Task A (Multi-Process):** Run `router ospf 1 vrf RED` and `router ospf 2 vrf BLUE`.
*   **Task B (Address Family):** Run `router ospf 100` and use `capability vrf-lite` inside specific VRFs (this is rarer but testable).
*   **Verify:** Ensure that routes learned in RED do not appear in BLUE.

* * *

#### **Phase 2: Route Leaking (The Hard Part)**

_This is the most common CCIE task: "Allow Red to talk to Blue, but only for specific subnets."_

**3\. Static Leaking (Point-to-Point)**

*   **Scenario:** Host A (VRF RED) needs to reach Host B (VRF BLUE).
*   **Task:**
    *   In VRF RED, write a static route: `ip route vrf RED 192.168.20.0 255.255.255.0 Ethernet0/1 192.168.1.254` (Where the next-hop IP is in the _Global_ table or another VRF).
    *   _Note:_ You often have to specify the egress interface **and** the next-hop IP for cross-VRF static routes to work.

**4\. MP-BGP Leaking (The "Correct" Way)**

*   **Concept:** Using Route Targets (RT) to import/export routes locally on the box, exactly how MPLS works, but without the MPLS tags.
*   **Task:**
    *   Configure `rd 1:1` for RED and `rd 2:2` for BLUE.
    *   Set RED to `route-target export 1:1`.
    *   Set BLUE to `route-target import 1:1`.
    *   Redistribute connected/static routes into BGP for both VRF address families.
*   **Verify:** See RED's routes appear in BLUE's routing table dynamically.

**5\. The "Shared Service" (Hub & Spoke)**

*   **Scenario:** VRF RED and VRF BLUE are customers. VRF SHARED contains a Domain Controller.
*   **Task:**
    *   Red and Blue cannot ping each other.
    *   Both Red and Blue can ping the Domain Controller.
    *   The Domain Controller can reply to both.
*   **Key:** This requires bidirectional leaking. Red imports Shared, Shared imports Red. (Repeat for Blue).

* * *

#### **Phase 3: Advanced & Security**

**6\. Front Door VRF (FVRF) for DMVPN**

*   **Concept:** This separates the "Underlay" (Internet transport) from the "Overlay" (Corporate data).
*   **Task:**
    *   Put the physical interface (e.g., `Gi0/1`) into `vrf definition INET`.
    *   Create a DMVPN Tunnel interface (`Tun0`) in the **Global** routing table (or a corporate VRF).
    *   **The Trick:** inside the tunnel configuration, use `tunnel vrf INET`.
*   **Why:** This prevents recursive routing loops where the tunnel tries to route to the tunnel destination through the tunnel itself.

**7\. VRF-Aware NAT**

*   **Scenario:** VRF RED needs to go out to the internet, which is in the Global routing table.
*   **Task:** Configure NAT such that traffic coming _from_ `ip nat inside` (VRF RED interface) is translated to an IP on the `ip nat outside` (Global interface).
*   **Command:** You often need `ip nat inside source list <ACL> interface <Global-Int> vrf RED`.

**8\. Management VRF w/ SSH**

*   **Task:** Create a VRF called `MGMT`. Put your management interface in it.
*   **Constraint:** You are trying to SSH into the router from your laptop. It fails.
*   **Fix:** You must tell the SSH server to listen on that VRF or use the specific command to SSH _out_: `ssh -l admin -vrf MGMT <ip>`.

### **Summary of Concepts to "Check Off"**

*   \[ \] `ip vrf` vs `vrf definition`
*   \[ \] `rd` (Route Distinguisher) vs `route-target`
*   \[ \] `ip vrf forwarding` (and the IP wipe effect)
*   \[ \] Leaking via Static Routes (Global to VRF / VRF to VRF)
*   \[ \] Leaking via MP-BGP (Import/Export Maps)
*   \[ \] Front Door VRFs (Tunnel protection)
*   \[ \] VRF-aware utilities (`ping vrf`, `traceroute vrf`, `tftp vrf`)