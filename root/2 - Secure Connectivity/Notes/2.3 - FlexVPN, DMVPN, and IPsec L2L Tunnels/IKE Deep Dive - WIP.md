# IKE Deep Dive - WIP
[https://www.ciscolive.com/on-demand/on-demand-library.html?search=ike&search=ike#/video/1636411415448001rnlc](https://www.ciscolive.com/on-demand/on-demand-library.html?search=ike&search=ike#/video/1636411415448001rnlc)

## Creation of IKE

1998: super high cost, hardware couldn't evolve. (hardware had to be replaced when new auth method) therefore ike had to be invented

*   success - went from des to 3des to aes
*   support certs/pki
*   catered to multiple situations

keys were generated on the fly

*   ike actually can have static keys manually defined
*   but this method allows for perfect forward secrecy

Prevents Man-in-the-middle attacks

IKE was hard for many to understand because of the number of RFCs to define it

*   went in the way for adoption
*   very abstract and complicated to understand

12 RFCs to define IPsec!

<figure class="image"><img style="aspect-ratio:701/401;" src="IKE Deep Dive - WIP_image.png" width="701" height="401"></figure>

**strict** distinction between control and data plane

*   IKE negotiates keys (ike is a root process that works at the same level of bgp or eigrp)
*   another set of protocols actually carry the data (works on the data plane like gre)

## ISAKMP

bgp comp: bgp just generates routes doesn't send any traffic

Phase 1:

*   definies control plane Phase 2:
*   push over data plan

2 modes:

main mode:

*   6 packet
*   full identity protection
*   better anti-dos protection (dos attack is kinda bs people dont really do it)

message 1/2

*   negotiate crypto attributes (auth metod, enc cypher, integrity hash, lifetime of sa, dh group)
*   not auth - not enc message 3/4
*   exchange dh key value, nonnce
*   nat detection happens here
*   further comms are enc and secure
*   peer not auth yet message 5/6
*   exchange certs
*   provide identity with psk or cert
*   validate previous messages - prevents session hijack
*   use udp/4500 if nat in mm3+4
*   encrypted - auth

Summary (3rtt): mm1+2 - negotiate crypto settings mm3+4 - key exchange mm5+6 - prove identity (encrypted - unauthenticated)

after that everything should be encrypted + authenticated

aggressive mode (1rtt-ish): am1 - send suggested crypto, dh value, init identity (unencrypt - unauth) am2 - accept paramaters from am1, resp identity, proof of resp identity (unencrypt - auth) am3 - sends full identity/proof of init identity

problems:

*   expose to mitm (bombard resp with init requests like tcp syn attack)
    *   bc dh is computed so early it takes longer to process this first packet

ikev1 - phase 2

control plane is secured now we need data plane channel the control and data plane dont have to be the same encryption methods

quick mode: qm1 - sends sa, nonce, key exchange (if pfs), traffic selector, nat info qm2 - yes or no? qm3 - ack

qm4 does exist, but no one uses it