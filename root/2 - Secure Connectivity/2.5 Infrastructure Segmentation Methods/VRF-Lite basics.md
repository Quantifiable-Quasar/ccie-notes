---
layout: default
title: VRF-Lite basics
parent: 2.5 Infrastructure Segmentation Methods
---
# VRF-Lite basics
## Overview

Virtual Routing and Forwarding (VRF) logically segments layer 3. This results in separate routing tables for each VRF. These kinda function like layer 3 VLANs. The lab is a full mest that uses GRE tunnels to showcase how this technology works. The underlay is in the 10.0.0.0/24 space, and resides in the global routing table. The 192.168.1X.0/24 and 10.10.10.0/24 networks reside in the RED VRF, and the 192.168.2X.0/24 and 10.10.20.0/24 networks reside in the BLUE VRF. 

<figure class="image"><img style="aspect-ratio:731/532;" src="1_VRF-Lite basics_image.png" width="731" height="532"></figure>

### Underlay Routing

The underlay routing protocol is iBGP, so that has to be set up to facilitate connectivity. Without that basic network connectivity, GRE tunnels could not be formed. 

```
iosv-0#show run | sec bgp
router bgp 65000
 bgp log-neighbor-changes
 network 1.1.1.1 mask 255.255.255.255
 neighbor 10.0.0.2 remote-as 65000
 neighbor 10.0.0.6 remote-as 65000
iosv-0#
```

### Create VRFs

Next, VRFs have to be created. The route descriptor provides a globally unique identifier for the VRF. Similarly to how a VLAN must be unique across the broadcast domain, a VRF must be unique across all internally managed networks. VRFs are then applied to interfaces, and in this scenario, loopbacks are used.  

```
iosv-0#show run vrf RED
Building configuration...

Current configuration : 567 bytes
vrf definition RED
 rd 65000:1
 !
 address-family ipv4
 exit-address-family
!
!
interface Loopback10
 vrf forwarding RED
 ip address 192.168.10.1 255.255.255.0
!
iosv-0#show run vrf BLUE
Building configuration...

Current configuration : 665 bytes
vrf definition BLUE
 rd 65000:2
 !
 address-family ipv4
 exit-address-family
!
!
interface Loopback20
 vrf forwarding BLUE
 ip address 192.168.20.1 255.255.255.0
```

### Create GRE tunnels

GRE tunnels are created to showcase how VRFs work. First, the tunnel is assigned to a VRF, then the source and destination are assigned. Since there are multiple tunnels originating and terminating at the same interfaces, a tunnel key is added so they remain unique. 

```
iosv-0#show run int tun 10
Building configuration...

Current configuration : 153 bytes
!
interface Tunnel10
 vrf forwarding RED
 ip address 10.10.10.1 255.255.255.252
 tunnel source Loopback0
 tunnel destination 2.2.2.2
 tunnel key 10
end

iosv-0#show run int tun 20
Building configuration...

Current configuration : 154 bytes
!
interface Tunnel20
 vrf forwarding BLUE
 ip address 10.10.20.1 255.255.255.252
 tunnel source Loopback0
 tunnel destination 2.2.2.2
 tunnel key 20
end

iosv-0#
```

### VRF routing

Now that the overlay exists, a routing protocol needs to be implemented so that traffic can span the network. To highlight the difference between the two BLUE used EIGRP and RED used OSPF. For EIGRP, the VRF gets it's own AS, and for OSPF, the VRF gets it's own router process. 

```
iosv-0#show run | sec eigrp
router eigrp VRF_BLUE
 !
 address-family ipv4 unicast vrf BLUE autonomous-system 20
  !
  topology base
  exit-af-topology
  network 10.10.20.0 0.0.0.255
  network 192.168.20.0
 exit-address-family
iosv-0#show run | sec ospf
router ospf 100 vrf RED
 network 10.10.10.0 0.0.0.255 area 0
 network 192.168.10.0 0.0.0.255 area 0
iosv-0#show run | sec eigrp
router eigrp VRF_BLUE
 !
 address-family ipv4 unicast vrf BLUE autonomous-system 20
  !
  topology base
  exit-af-topology
  network 10.10.20.0 0.0.0.255
  network 192.168.20.0
 exit-address-family
iosv-0#
```

### Verify

The VRFs can be verified by viewing the routing tables for each VRF. As seen below, BGP, the underlay protocol, is only accessible through the global routing table. EIGRP is only available through BLUE and OSPF through RED. 

```
iosv-0#show ip route
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      1.0.0.0/32 is subnetted, 1 subnets
C        1.1.1.1 is directly connected, Loopback0
      2.0.0.0/32 is subnetted, 1 subnets
B        2.2.2.2 [200/0] via 10.0.0.2, 00:27:28
      3.0.0.0/32 is subnetted, 1 subnets
B        3.3.3.3 [200/0] via 10.0.0.6, 00:27:28
      10.0.0.0/8 is variably subnetted, 4 subnets, 2 masks
C        10.0.0.0/30 is directly connected, GigabitEthernet0/1
L        10.0.0.1/32 is directly connected, GigabitEthernet0/1
C        10.0.0.4/30 is directly connected, GigabitEthernet0/2
L        10.0.0.5/32 is directly connected, GigabitEthernet0/2
iosv-0#show ip route vrf RED

Routing Table: RED
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
C        10.10.10.0/30 is directly connected, Tunnel10
L        10.10.10.1/32 is directly connected, Tunnel10
C        10.10.10.4/30 is directly connected, Tunnel12
L        10.10.10.5/32 is directly connected, Tunnel12
O        10.10.10.8/30 [110/2000] via 10.10.10.6, 00:15:10, Tunnel12
                       [110/2000] via 10.10.10.2, 00:19:09, Tunnel10
      192.168.10.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.10.0/24 is directly connected, Loopback10
L        192.168.10.1/32 is directly connected, Loopback10
      192.168.11.0/32 is subnetted, 1 subnets
O        192.168.11.1 [110/1001] via 10.10.10.2, 00:18:58, Tunnel10
      192.168.13.0/32 is subnetted, 1 subnets
O        192.168.13.1 [110/1001] via 10.10.10.6, 00:12:58, Tunnel12
iosv-0#show ip route vrf BLUE

Routing Table: BLUE
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is not set

      10.0.0.0/8 is variably subnetted, 5 subnets, 2 masks
C        10.10.20.0/30 is directly connected, Tunnel20
L        10.10.20.1/32 is directly connected, Tunnel20
C        10.10.20.4/30 is directly connected, Tunnel22
L        10.10.20.5/32 is directly connected, Tunnel22
D        10.10.20.8/30 [90/102400000] via 10.10.20.2, 00:22:57, Tunnel20
      192.168.20.0/24 is variably subnetted, 2 subnets, 2 masks
C        192.168.20.0/24 is directly connected, Loopback20
L        192.168.20.1/32 is directly connected, Loopback20
D     192.168.21.0/24 [90/76800640] via 10.10.20.2, 00:22:46, Tunnel20
D     192.168.23.0/24 [90/76800640] via 10.10.20.6, 00:12:00, Tunnel22
iosv-0# 
```