---
layout: default
title: Cert based IPsec
parent: 2.2 - IOS CA for VPN Auth
---
# Cert based IPsec 
\[NOTE\]: This note needs cleaned up and redone

[https://www.cisco.com/c/en/us/td/docs/ios/security/configuration/guide/sec\_cfg\_cert\_auth\_io.html](https://www.cisco.com/c/en/us/td/docs/ios/security/configuration/guide/sec_cfg_cert_auth_io.html)

## Overview

The above note details how to set up a CA, but doesn't do anything with the certs. This note will go into the application of the certs to a IPsec VPN tunnel. 

### SCEP cert enrollment

this was covered before, but here it is again

```
iosv-1(config)#ip domain-n lab.lcl
iosv-1(config)#crypto key gen rsa mod 2048 label VPN_KEY
The name for the keys will be: VPN_KEY

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 3 seconds)

iosv-1(config)#
*Dec 30 09:20:23.408: %SSH-5-ENABLED: SSH 1.99 has been enabled
iosv-1(config)#crypto pki cert map VPN_MAP 1
iosv-1(ca-certificate-map)#issuer-name co cn=CA
iosv-1(ca-certificate-map)#exit
iosv-1(config)#crypto pki trust VPN_TP
iosv-1(ca-trustpoint)#enrollment url http://10.0.0.1:80
iosv-1(ca-trustpoint)#serial-number none
iosv-1(ca-trustpoint)#ip-address none
iosv-1(ca-trustpoint)#subject-name cn=iosv1.lab.lcl,c=US
iosv-1(ca-trustpoint)#rev none
iosv-1(ca-trustpoint)#rsakey VPN_KEY
iosv-1(ca-trustpoint)#exit
iosv-1(config)#ip route 10.0.0.1 255.255.255.255 192.168.1.1
iosv-1(config)#
```

```
iosv-1(config-if)#crypto pki auth VPN_TP            
Certificate has the following attributes:
       Fingerprint MD5: 0813A2CD A3577F5B B8444C8F 093BDB2E 
      Fingerprint SHA1: 50CB1BE1 F8A16D5C 0DB3BC72 E6D422B0 82D7F7CD 

% Do you accept this certificate? [yes/no]: yes
Trustpoint CA certificate accepted.
iosv-1(config)#crypto pki enroll VPN_TP
%
% Start certificate enrollment .. 
% Create a challenge password. You will need to verbally provide this
   password to the CA Administrator in order to revoke your certificate.
   For security reasons your password will not be saved in the configuration.
   Please make a note of it.

Password: 
Re-enter password: 

% The subject name in the certificate will include: cn=iosv1.lab.lcl,c=US
% The subject name in the certificate will include: iosv-1.lab.lcl
Request certificate from CA? [yes/no]: yes
% Certificate request sent to Certificate Authority
% The 'show crypto pki certificate verbose VPN_TP' commandwill show the fingerprint.

iosv-1(config)#
```

### Set up the tunnel

```
crypto isakmp policy 15
 encr 3des
 hash md5
 group 2
 lifetime 5000
!
!
!
crypto ipsec transform-set tform esp-3des esp-sha-hmac 
 mode tunnel
!
!
!
crypto map map-to-remotesite 10 ipsec-isakmp 
 set peer 192.168.1.11
 set transform-set tform 
 match address 123
!
!
!
interface Loopback1
 ip address 10.0.0.10 255.255.255.255
!
!
!
interface GigabitEthernet0/2
 ip address 192.168.1.10 255.255.255.0
 duplex auto
 speed auto
 media-type rj45
 crypto map map-to-remotesite
!
!
!
ip route 10.0.0.1 255.255.255.255 192.168.1.1
```