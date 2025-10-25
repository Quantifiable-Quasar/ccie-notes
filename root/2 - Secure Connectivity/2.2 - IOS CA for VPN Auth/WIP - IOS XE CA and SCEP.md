---
layout: default
title: WIP - IOS XE CA and SCEP
parent: 2.2 - IOS CA for VPN Auth
---
# WIP - IOS XE CA and SCEP
## Overview

The goal of this lab is to implement a certificate based IPsec tunnel using the IOS router as the CA. Using the topology below, first the CA will be configured, then RTR2 will be enrolled and a site-to-site VPN will be established. Finally, ASA1 will establish a site-to-site VPN with the CA-RTR as well. 

<figure class="image"><img style="aspect-ratio:410/115;" src="WIP - IOS XE CA and SCEP_i.png" width="410" height="115"></figure>

1.  Establish CA
2.  Enroll RTR2 and ASA1 with SCEP over HTTP
3.  Configure the VPN tunnel using the keys as the identity source

## Establish CA

To establish the CA the HTTP server needs to be started. SCEP works over HTTP, so after generating the CA keys, we will communicate over HTTP. 

### Generate the Keys

Here, there are some interesting error warnings. To be honest, I have no idea why it says that the crypto commands will be deprecated. I don't know how else to do any of this stuff, so I hope that's not true. 

```
CA-RTR(config)#crypto key generate rsa general-keys label CA-KEY modulus 2048
The name for the keys will be: CA-KEY

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 1 seconds)

CA-RTR(config)#
*Oct 25 14:35:49.551: %PARSER-5-HIDDEN: Warning!!! ' crypto key generate rsa general-keys label * modulus 2048' is a hidden command. Use of this command is not recommended/supported and will be removed in future.
CA-RTR(config)#
*Oct 25 14:35:50.860: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named CA-KEY has been generated or imported by crypto-engine
*Oct 25 14:35:50.860: %SSH-5-ENABLED: SSH 2.0 has been enabled
*Oct 25 14:35:51.603: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named CA-KEY.server has been generated or imported by crypto-engine
```

### Start CA Server

```
CA-RTR(config)#ip http server
CA-RTR(config)#crypto pki server CA-RTR
CA-RTR(cs-server)#hash sha256
CA-RTR(cs-server)#database level complete
CA-RTR(cs-server)#database archive pkcs12 pass cisco123
CA-RTR(cs-server)#issuer-name cn=CA-RTR
CA-RTR(cs-server)#grant auto 
CA-RTR(cs-server)#
*Oct 25 15:42:52.560: %PKI-6-CS_GRANT_AUTO: All enrollment requests will be automatically granted.        
CA-RTR(cs-server)#lifetime ca-certificate 3650
CA-RTR(cs-server)#lifetime certificate 1095
CA-RTR(cs-server)#auto-rollover 365
CA-RTR(cs-server)#database url nvram:
*Oct 25 14:40:00.483: %PKI-6-CS_GRANT_AUTO: All enrollment requests will be automatically granted.
CA-RTR(cs-server)#no shut            
%Some server settings cannot be changed after CA certificate generation.
% Exporting Certificate Server signing certificate and keys...

% Certificate Server enabled.
CA-RTR(cs-server)#
*Oct 25 15:44:22.730: CRYPTO_CS: updated crl in memory .. 
SEQ(342)
    SEQ(64)
        SEQ(13)
            OID(9):SHA Signature 1.2.840.113549.1.1.5 
            NULL
            END
        SEQ(17)
            SET(15)
                SEQ(13)
                    OID(3):Common Name 2.5.4.3 
                    PRT(6):CA-RTR
                    END
                END
            END
        UTC(13):251025154422Z
        UTC(13):251025214422Z
        END
    SEQ(13)
        OID(9):SHA Signature 1.2.840.113549.1.1.5 
        NULL
        END
    BIT(256<-0>): 
         00 80 4C 8D 44 9A 73 26 51 B8 3B 49 AE 8E B0 76 
         A0 F9 60 61 C3 06 FF 9E F6 08 AC E7 86 8E 73 CD 
         CF BC 92 A4 09 D8 36 27 C0 EE B2 D1 AC 0B A8 6C 
         C3 0B 41 C6 60 AB C9 5B 64 E1 80 66 60 A3 85 EE 
         30 49 18 75 30 E1 A5 16 A4 F4 3F 03 64 D7 F4 5D 
         CA 89 90 DC 39 94 33 64 3C B0 39 BB 33 79 7D 01 
         49 AA 13 36 05 9D 27 AE 76 FC 1D 86 D2 F0 36 49 
         04 CD 53 55 E7 A4 12 1F DB 37 69 DA 70 28 26 A4 
         E8 2B 9C 31 84 82 AD 1D B9 64 1E 96 72 59 57 31 
         7A F3 1F 2E 95 0F A6 78 B9 AB 3F 41 38 90 1B AE 
         1D E5 05 BF 73 E6 DD 37 27 CE BC ED 4E 3C 50 6C 
         52 95 77 E7 AF 5A 7D DC 12 0C CD 1E 89 69 90 E7 
         C2 6E AA C3 74 92 8A D2 A1 7C 9F 12 4D 2E 17 93 
         8E 54 99 0C A3 C2 01 E0 02 30 0A E0 68 5A 48 11 
         74 9B 5D B7 3F 8C C6 13 38 A4 5A EE 59 E5 8C 64 
         81 01 C4 72 93 06 FC A6 03 20 2A 9D 67 BC 2C 5D 
         D2                                              
    END

CA-RTR(cs-server)#
*Oct 25 15:44:22.745: %PKI-6-CS_ENABLED: Certificate server now enabled.
CA-RTR(cs-server)#
```

Now that the root CA keys have been generated, the server to communicate with clients needs to be started. This is through the basic HTTP server built into the router.

## Enroll a client

Now that the server is configured, a client needs to be configured to use the CA. 

### IOS XE

```
RTR2(config)#crypto key generate rsa general-keys label RTR2-KEY mod 2048
The name for the keys will be: RTR2-KEY

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 1 seconds)

RTR2(config)#
*Oct 25 14:44:20.770: %PARSER-5-HIDDEN: Warning!!! ' crypto key generate rsa general-keys label * modulus 2048' is a hidden command. Use of this command is not recommended/supported and will be removed in future.
RTR2(config)#
*Oct 25 14:44:21.793: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named RTR2-KEY has been generated or imported by crypto-engine
*Oct 25 14:44:21.794: %SSH-5-ENABLED: SSH 2.0 has been enabled
*Oct 25 14:44:22.709: %CRYPTO_ENGINE-5-KEY_ADDITION: A key named RTR2-KEY.server has been generated or imported by crypto-engine
RTR2(config)#
RTR2(config)#crypto pki trustpoint VPN-CA
RTR2(ca-trustpoint)#
*Oct 25 14:42:39.586: %PKI-6-TRUSTPOINT_CREATE: Trustpoint: VPN-CA created succesfully
RTR2(ca-trustpoint)#enrollment url http://10.0.0.1
RTR2(ca-trustpoint)#subject-name CN=CA-RTR
RTR2(ca-trustpoint)#subject-name CN=RTR2  
RTR2(ca-trustpoint)#rsakeypair RTR2-KEY
RTR2(ca-trustpoint)#revocation-check none
RTR2(ca-trustpoint)#password 0 cisco123
RTR2(ca-trustpoint)#exit
RTR2(config)#
```