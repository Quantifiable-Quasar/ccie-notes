---
layout: default
title: IOSv CA
parent: 2.2 - IOS CA for VPN Auth
---
# IOSv CA
## Overview

[https://www.cisco.com/c/en/us/support/docs/security-vpn/public-key-infrastructure-pki/211333-IOS-PKI-Deployment-Guide-Initial-Design.html](https://www.cisco.com/c/en/us/support/docs/security-vpn/public-key-infrastructure-pki/211333-IOS-PKI-Deployment-Guide-Initial-Design.html)

This lab is to practice the process of generating certs from a router. It only has one server and one client. [This is the source I'm working from.](https://integratingit.wordpress.com/2019/03/26/cisco-ios-certificate-authority/) The diagram shows three routers, with the switch representing the internet. This lab will include both manual copy/paste cert enrollment and SCEP. The limitation of SCEP is the requirement of network connectivity to the CA which is limited over the internet. 

<figure class="image"><img style="aspect-ratio:283/270;" src="1_IOSv CA_image.png" width="283" height="270"></figure>

1.  Generate key pairs
2.  Define PKI server
3.  SCEP
    1.  Create keypair
    2.  Certificate map
    3.  Trustpoint
    4.  Request CA certificate
    5.  Request identity certificate
4.  Manual Enrollment
    1.  Create keypair
    2.  Certificate Map
    3.  Trustpoint
    4.  Request CA certificate
    5.  Request identity certificate

### CA Configuration

The Certificate Authority needs to be configured to house the root cert and listen for incoming connections. This one configuration will support both the SCEP and terminal enrollment methods.

#### RSA keypair generation

```
CA(config)#crypto key generate rsa modulus 2048 label PKI_SERVER exportable
The name for the keys will be: PKI_SERVER

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be exportable...
[OK] (elapsed time was 3 seconds)

CA(config)#
```

#### Server Settings

Several things need to be specified in order for this to work properly. First, the http server needs to be enabled so SCEP will work in the future. Database refers to how many files will be created when a client is enrolled, and then how will they be encrypted. The cdp-url is in reference to the CRL list. I don't plan to actually use that in this lab. The database is set to be stored in NVRAM, but the recommendation is to store the database on an external server. Finally, the server has to be enabled.

```
CA(config)#ip http server
CA(config)#crypto pki server PKI_SERVER
CA(cs-server)#database level complete
CA(cs-server)#database archive pkcs12 password Cisco123
CA(cs-server)#issuer-name CN=CA.lab.lcl,C=US
CA(cs-server)#grant auto
CA(cs-server)#
*Dec 30 07:04:54.072: %PKI-6-CS_GRANT_AUTO: All enrollment requests will be automatically granted. 
CA(cs-server)#cdp-url http://10.0.0.1/cgi-bin/pkiclient.exe
CA(cs-server)#auto-rollover 1
CA(cs-server)#database url ser nvram:
CA(cs-server)#no shut
%Some server settings cannot be changed after CA certificate generation.
% Exporting Certificate Server signing certificate and keys...

% Certificate Server enabled.
CA(cs-server)#
```

### SCEP Client

thing

#### RSA keypair generation

```
SCEP(config)#crypto key generate rsa modulus 2048 label SCEP_KEY
The name for the keys will be: SCEP_KEY

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 3 seconds)

SCEP(config)#
```

#### Certificate Setup

Now that the server has been set up, the client can be enrolled. Fist a certificate map is created, and then a trustpoint. This is a fairly bare bones config.

```
SCEP(config)#crypto pki certificate map CERT_MAP 1
SCEP(ca-certificate-map)#issuer-name co cn = ca
SCEP(ca-certificate-map)#exit
SCEP(config)#crypto pki trustpoint CERT_TP
SCEP(ca-trustpoint)#enrollment url http://10.0.0.1:80
SCEP(ca-trustpoint)#serial-number none
SCEP(ca-trustpoint)#ip-address none
SCEP(ca-trustpoint)#subject-name cn=scep.lab.lcl,c=US  
SCEP(ca-trustpoint)#revocation-check none
SCEP(ca-trustpoint)#rsakeypair SCEP_KEY
SCEP(ca-trustpoint)#exit
SCEP(config)#
```

#### Enrollment with CA over SCEP

Once the trustpoint has been configured, the certs can be sent. First, the trustpoint is authenticated by receiving and verifying the CA's cert. Then, the client is enrolled in the trustpoint and the identity certificate is issued. 

```
SCEP(config)#crypto pki authenticate CERT_TP              
Certificate has the following attributes:
       Fingerprint MD5: 0813A2CD A3577F5B B8444C8F 093BDB2E 
      Fingerprint SHA1: 50CB1BE1 F8A16D5C 0DB3BC72 E6D422B0 82D7F7CD 

% Do you accept this certificate? [yes/no]: yes
Trustpoint CA certificate accepted.
SCEP(config)#crypto pki enroll CERT_TP
%
% Start certificate enrollment .. 
% Create a challenge password. You will need to verbally provide this
   password to the CA Administrator in order to revoke your certificate.
   For security reasons your password will not be saved in the configuration.
   Please make a note of it.

Password: 
Re-enter password: 

% The subject name in the certificate will include: cn=scep.lab.lcl,c=US
% The subject name in the certificate will include: SCEP
Request certificate from CA? [yes/no]: yes
% Certificate request sent to Certificate Authority
% The 'show crypto pki certificate verbose CERT_TP' commandwill show the fingerprint.

SCEP(config)#
*Dec 30 07:19:49.124: CRYPTO_PKI:  Certificate Request Fingerprint MD5: 45C423D0 65B51004 1A399638 7AE6630E 
*Dec 30 07:19:49.145: CRYPTO_PKI:  Certificate Request Fingerprint SHA1: 33788EFA B06ADAA0 2494A2F6 FAD7B120 8F62246A 
*Dec 30 07:19:56.398: %PKI-6-CERTRET: Certificate received from Certificate Authority
SCEP(config)#
```

### Manual Client

#### RSA keygen

```
Manual(config)#crypto key generate rsa modulus 2048 label CERT_KEY
The name for the keys will be: CERT_KEY

% The key modulus size is 2048 bits
% Generating 2048 bit RSA keys, keys will be non-exportable...
[OK] (elapsed time was 5 seconds)

Manual(config)#
```

#### Certificate Setup

This is very similar to the SECP client, but the method is different. 

```
Manual(config)#crypto pki certificate map CERT_MAP 1
Manual(ca-certificate-map)#issuer-name co cn = ca
Manual(ca-certificate-map)#exit
Manual(config)#crypto pki trustpoint CERT_TP
Manual(ca-trustpoint)#enrollment terminal
Manual(ca-trustpoint)#serial-number none
Manual(ca-trustpoint)#ip-address none
Manual(ca-trustpoint)#subject-name cn=Manual,c=US
Manual(ca-trustpoint)#revocation-check crl
Manual(ca-trustpoint)#rsakeypair CERT_KEY
Manual(ca-trustpoint)#
```

#### Request the CA Certificate

Here, the client needs to establish a trust relationship with the CA. The cert is imported by copy/paste from the CA terminal to the client router's terminal. 

```
CA(config)#crypto pki export PKI_SERVER pem terminal
% The specified trustpoint is not enrolled (PKI_SERVER).
% Only export the CA certificate in PEM format.
% CA certificate:
-----BEGIN CERTIFICATE-----
MIIDIjCCAgqgAwIBAgIBATANBgkqhkiG9w0BAQQFADAiMQswCQYDVQQGEwJVUzET
MBEGA1UEAxMKQ0EubGFiLmxjbDAeFw0yNTEyMzAwNzA1NDNaFw0yODEyMjkwNzA1
NDNaMCIxCzAJBgNVBAYTAlVTMRMwEQYDVQQDEwpDQS5sYWIubGNsMIIBIjANBgkq
hkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA05BwKW/Rw0GvLc0EGwKAxNQdWjoX5rdw
fSlnnMCT5r1OcaYFqwEv2t67y+04LavDHhCAfpJhMYDRhS1LtAYLjsGsCfyHKK/L
mKAgx9m5gVKNfw0fBa1EYHGgdXnIH141cUCVADUVzwP5MsKJyxRp1jtE73apCHEl
kUkfZ2NB7XnUshQIODn5Wi72ks9lOnwnJt3h7vE7jZYz/5tP0ZvtPhDmISUynmhl
qwh1lFZz3zJCgV81ek/EK5CK0mDffabV4/q2i2o8K1eU7B3l3aaQOt2W21WicbE8
T+eBc8vMYYPpefayIOrrzwvJEW74ts4bbvh8/QjFmHlq4uyUZvuHEQIDAQABo2Mw
YTAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBhjAfBgNVHSMEGDAWgBSy
f/OKC+M3ze7TMHgNW60twirVDDAdBgNVHQ4EFgQUsn/zigvjN83u0zB4DVutLcIq
1QwwDQYJKoZIhvcNAQEEBQADggEBAE1DrtBkxDSGRCKOnLkRSF2G+yA6CrqpGp+i
P45zj2wEoGJPoYTkd4YJqpj02DLgy65ZjDG8NP3BOBKAaQ6sdKMnVFVW8rcI1Paj
d8t24nlpxx+NBGi77aAqFE4HhCHr32YyCkmLQtg5GGlQ9KkOWFVzj7fVve5vrbwc
5XymRh57U8gfJSOaK+uwezGf/DVjZ97JYcJxMOYHH698QY4VNcQYREyjmTYRkJ0Q
0KBtDKDWpw3iP+D6RVbS8KRrzaDzftj4mwShXDM+DKk9KP+Vd0UVDUrFe+/AjREu
Oc854bZoSo0zdb7H3TBexP5fAMf443k9lp72CztVsRHXGTVdCcY=
-----END CERTIFICATE-----

CA(config)# 
```

Pasting that certificate as the input to the below command will successfully authenticate the trustpoint. 

```
Manual(config)#crypto pki authenticate CERT_TP

Enter the base 64 encoded CA certificate.
End with a blank line or the word "quit" on a line by itself

-----BEGIN CERTIFICATE-----
MIIDIjCCAgqgAwIBAgIBATANBgkqhkiG9w0BAQQFADAiMQswCQYDVQQGEwJVUzET
MBEGA1UEAxMKQ0EubGFiLmxjbDAeFw0yNTEyMzAwNzA1NDNaFw0yODEyMjkwNzA1
NDNaMCIxCzAJBgNVBAYTAlVTMRMwEQYDVQQDEwpDQS5sYWIubGNsMIIBIjANBgkq
hkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA05BwKW/Rw0GvLc0EGwKAxNQdWjoX5rdw
fSlnnMCT5r1OcaYFqwEv2t67y+04LavDHhCAfpJhMYDRhS1LtAYLjsGsCfyHKK/L
mKAgx9m5gVKNfw0fBa1EYHGgdXnIH141cUCVADUVzwP5MsKJyxRp1jtE73apCHEl
kUkfZ2NB7XnUshQIODn5Wi72ks9lOnwnJt3h7vE7jZYz/5tP0ZvtPhDmISUynmhl
qwh1lFZz3zJCgV81ek/EK5CK0mDffabV4/q2i2o8K1eU7B3l3aaQOt2W21WicbE8
T+eBc8vMYYPpefayIOrrzwvJEW74ts4bbvh8/QjFmHlq4uyUZvuHEQIDAQABo2Mw
YTAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIBhjAfBgNVHSMEGDAWgBSy
f/OKC+M3ze7TMHgNW60twirVDDAdBgNVHQ4EFgQUsn/zigvjN83u0zB4DVutLcIq
1QwwDQYJKoZIhvcNAQEEBQADggEBAE1DrtBkxDSGRCKOnLkRSF2G+yA6CrqpGp+i
P45zj2wEoGJPoYTkd4YJqpj02DLgy65ZjDG8NP3BOBKAaQ6sdKMnVFVW8rcI1Paj
d8t24nlpxx+NBGi77aAqFE4HhCHr32YyCkmLQtg5GGlQ9KkOWFVzj7fVve5vrbwc
5XymRh57U8gfJSOaK+uwezGf/DVjZ97JYcJxMOYHH698QY4VNcQYREyjmTYRkJ0Q
0KBtDKDWpw3iP+D6RVbS8KRrzaDzftj4mwShXDM+DKk9KP+Vd0UVDUrFe+/AjREu
Oc854bZoSo0zdb7H3TBexP5fAMf443k9lp72CztVsRHXGTVdCcY=
-----END CERTIFICATE-----

Certificate has the following attributes:
       Fingerprint MD5: 0813A2CD A3577F5B B8444C8F 093BDB2E 
      Fingerprint SHA1: 50CB1BE1 F8A16D5C 0DB3BC72 E6D422B0 82D7F7CD 

% Do you accept this certificate? [yes/no]: yes
Trustpoint CA certificate accepted.
% Certificate successfully imported

Manual(config)#
```

#### Request the identity certificate

Now that the CA is trusted the identity certificate needs to be issues. An identity cert verifies this router's identity. The process is to first generate a Certificate Signing Request (CSR) by enrolling the router with the trustpoint. Next, the CSR is signed by the CA which produces the signed certificate that authenticates the router. 

This is the generation of the CSR by the client router.

```
Manual(config)#crypto pki enroll CERT_TP
% Start certificate enrollment .. 

% The subject name in the certificate will include: cn=Manual,c=US
% The subject name in the certificate will include: Manual
Display Certificate Request to terminal? [yes/no]: yes
Certificate Request follows:

MIICmzCCAYMCAQAwNTELMAkGA1UEBhMCVVMxDzANBgNVBAMTBk1hbnVhbDEVMBMG
CSqGSIb3DQEJAhYGTWFudWFsMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEAuw0+ui2uAuUyXcyenKbVS1IZisVPgrV1w1bJX/Dx0B+H7sViom9D4fHvWvYJ
BFUJuvPIYX5Ww3JWkK/s9L7ZuwNLxajoD04AAX6jR9R5MIS04K0BNY1UW802Vo3g
wjRkv6LynnkUU31TnAbLyzGS4Z/rwDlNJF4QCfyRMoilug2iuAlW64uNwN6+hWnB
+Wa2q5UcGaUV+QZP/t1UnKXA+40ipdfORDC5hIoIHPsNQIBpHzOYPdReGlY+KwjS
1MC4TYpda94J7EwkeLgsZJuj4yE9VPMay7jOL0ZkxfFZNG2NQ+5tLLiY/K77F91o
s4jIxqohv8EHgA0XH+2Z+dyOVwIDAQABoCEwHwYJKoZIhvcNAQkOMRIwEDAOBgNV
HQ8BAf8EBAMCBaAwDQYJKoZIhvcNAQEFBQADggEBAFmNqYSLVAURdZbTE/VMAyYS
wZ2UGM+a1EN73WG8LKCdLv8B24jlJ4XL2A0pjUHKyTmIbYPgPyBCjldamniDhbOg
y5wKHDFa27BjtQxUsyuMxzWC0RP7qDZenXjfWJZM4CG58CrkawUD4daGecVOPjhd
gjXECysF4mwty0AVR0zBofr9jIJBmZIZWPxmRKflljYXCwDh4Qw02M6k1v3+HjvW
OW2PzQYQhPnSGkbjrCPcp92qEB5mla1pOXSfJ4zwkf/51EKjRt+Mrbj/Q2MtkNKG
kHZwXDL4wSBVsHSLN6kvOv6twjBjS28uVULkYzXFEJByggGhzJz/XoRZk8bFI+U=

---End - This line not part of the certificate request---

Redisplay enrollment request? [yes/no]: 
```

This is the CSR being signed by the CA. The cert was copy/pasted in manually. 

```


CA#crypto pki server PKI_SERVER request pkcs10 terminal
PKCS10 request in base64 or pem

% Enter Base64 encoded or PEM formatted PKCS10 enrollment request.
% End with a blank line or "quit" on a line by itself.
MIICmzCCAYMCAQAwNTELMAkGA1UEBhMCVVMxDzANBgNVBAMTBk1hbnVhbDEVMBMG
CSqGSIb3DQEJAhYGTWFudWFsMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKC
AQEAuw0+ui2uAuUyXcyenKbVS1IZisVPgrV1w1bJX/Dx0B+H7sViom9D4fHvWvYJ
BFUJuvPIYX5Ww3JWkK/s9L7ZuwNLxajoD04AAX6jR9R5MIS04K0BNY1UW802Vo3g
wjRkv6LynnkUU31TnAbLyzGS4Z/rwDlNJF4QCfyRMoilug2iuAlW64uNwN6+hWnB
+Wa2q5UcGaUV+QZP/t1UnKXA+40ipdfORDC5hIoIHPsNQIBpHzOYPdReGlY+KwjS
1MC4TYpda94J7EwkeLgsZJuj4yE9VPMay7jOL0ZkxfFZNG2NQ+5tLLiY/K77F91o
s4jIxqohv8EHgA0XH+2Z+dyOVwIDAQABoCEwHwYJKoZIhvcNAQkOMRIwEDAOBgNV
HQ8BAf8EBAMCBaAwDQYJKoZIhvcNAQEFBQADggEBAFmNqYSLVAURdZbTE/VMAyYS
wZ2UGM+a1EN73WG8LKCdLv8B24jlJ4XL2A0pjUHKyTmIbYPgPyBCjldamniDhbOg
y5wKHDFa27BjtQxUsyuMxzWC0RP7qDZenXjfWJZM4CG58CrkawUD4daGecVOPjhd
gjXECysF4mwty0AVR0zBofr9jIJBmZIZWPxmRKflljYXCwDh4Qw02M6k1v3+HjvW
OW2PzQYQhPnSGkbjrCPcp92qEB5mla1pOXSfJ4zwkf/51EKjRt+Mrbj/Q2MtkNKG
kHZwXDL4wSBVsHSLN6kvOv6twjBjS28uVULkYzXFEJByggGhzJz/XoRZk8bFI+U=

% Granted certificate:
MIIDYDCCAkigAwIBAgIBAzANBgkqhkiG9w0BAQQFADAiMQswCQYDVQQGEwJVUzET
MBEGA1UEAxMKQ0EubGFiLmxjbDAeFw0yNTEyMzAwNzQ1MjZaFw0yNjEyMzAwNzQ1
MjZaMDUxCzAJBgNVBAYTAlVTMQ8wDQYDVQQDEwZNYW51YWwxFTATBgkqhkiG9w0B
CQIWBk1hbnVhbDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALsNProt
rgLlMl3Mnpym1UtSGYrFT4K1dcNWyV/w8dAfh+7FYqJvQ+Hx71r2CQRVCbrzyGF+
VsNyVpCv7PS+2bsDS8Wo6A9OAAF+o0fUeTCEtOCtATWNVFvNNlaN4MI0ZL+i8p55
FFN9U5wGy8sxkuGf68A5TSReEAn8kTKIpboNorgJVuuLjcDevoVpwflmtquVHBml
FfkGT/7dVJylwPuNIqXXzkQwuYSKCBz7DUCAaR8zmD3UXhpWPisI0tTAuE2KXWve
CexMJHi4LGSbo+MhPVTzGsu4zi9GZMXxWTRtjUPubSy4mPyu+xfdaLOIyMaqIb/B
B4ANFx/tmfncjlcCAwEAAaOBjTCBijA4BgNVHR8EMTAvMC2gK6AphidodHRwOi8v
MTcyLjIxLjAuMS9jZ2ktYmluL3BraWNsaWVudC5leGUwDgYDVR0PAQH/BAQDAgWg
MB8GA1UdIwQYMBaAFLJ/84oL4zfN7tMweA1brS3CKtUMMB0GA1UdDgQWBBTkOHCY
+EaX+AQt5e0t9RSpSTpF1jANBgkqhkiG9w0BAQQFAAOCAQEAgenRlRIC/il97UiK
LX7JQCASCpe2tKGUBhp5TP6zfAmaG54ymdDaUL9WMfz6ojiNassd8PWcXoJFF0g6
FCzC/CkMUXpzg0czXWxfqoyG4R25FoHwuqDwiVPgrsbZBObIKsSLfYz3eh+21Cid
a8u+oL3HEJ1MrDO3A4cvgyF/zBnNjq9TLyU9SxGz4tE9cLkzKSyWxmawnicFoWf4
B8xZ493wx4yEcjfOKnO8KNxfPXtRKFe/0geH+xWkJ1V/Wd5GPHTuCpmasPDuNA3s
82QKietTC1nOogT7YY10bC1TxYOL4ZOpwlY0fv3s4+lzwheTS7D2/Wt2hprbHhq8
kz5mvA==

CA#
```

The “granted certificate” was then copied and pasted into the terminal of the client router. This resulted in the fully signed identity cert being imported. 

```
Manual(config)#crypto pki import CERT_TP certificate

Enter the base 64 encoded certificate.
End with a blank line or the word "quit" on a line by itself

MIIDYDCCAkigAwIBAgIBAzANBgkqhkiG9w0BAQQFADAiMQswCQYDVQQGEwJVUzET
MBEGA1UEAxMKQ0EubGFiLmxjbDAeFw0yNTEyMzAwNzQ1MjZaFw0yNjEyMzAwNzQ1
MjZaMDUxCzAJBgNVBAYTAlVTMQ8wDQYDVQQDEwZNYW51YWwxFTATBgkqhkiG9w0B
CQIWBk1hbnVhbDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALsNProt
rgLlMl3Mnpym1UtSGYrFT4K1dcNWyV/w8dAfh+7FYqJvQ+Hx71r2CQRVCbrzyGF+
VsNyVpCv7PS+2bsDS8Wo6A9OAAF+o0fUeTCEtOCtATWNVFvNNlaN4MI0ZL+i8p55
FFN9U5wGy8sxkuGf68A5TSReEAn8kTKIpboNorgJVuuLjcDevoVpwflmtquVHBml
FfkGT/7dVJylwPuNIqXXzkQwuYSKCBz7DUCAaR8zmD3UXhpWPisI0tTAuE2KXWve
CexMJHi4LGSbo+MhPVTzGsu4zi9GZMXxWTRtjUPubSy4mPyu+xfdaLOIyMaqIb/B
B4ANFx/tmfncjlcCAwEAAaOBjTCBijA4BgNVHR8EMTAvMC2gK6AphidodHRwOi8v
MTcyLjIxLjAuMS9jZ2ktYmluL3BraWNsaWVudC5leGUwDgYDVR0PAQH/BAQDAgWg
MB8GA1UdIwQYMBaAFLJ/84oL4zfN7tMweA1brS3CKtUMMB0GA1UdDgQWBBTkOHCY
+EaX+AQt5e0t9RSpSTpF1jANBgkqhkiG9w0BAQQFAAOCAQEAgenRlRIC/il97UiK
LX7JQCASCpe2tKGUBhp5TP6zfAmaG54ymdDaUL9WMfz6ojiNassd8PWcXoJFF0g6
FCzC/CkMUXpzg0czXWxfqoyG4R25FoHwuqDwiVPgrsbZBObIKsSLfYz3eh+21Cid
a8u+oL3HEJ1MrDO3A4cvgyF/zBnNjq9TLyU9SxGz4tE9cLkzKSyWxmawnicFoWf4
B8xZ493wx4yEcjfOKnO8KNxfPXtRKFe/0geH+xWkJ1V/Wd5GPHTuCpmasPDuNA3s
82QKietTC1nOogT7YY10bC1TxYOL4ZOpwlY0fv3s4+lzwheTS7D2/Wt2hprbHhq8
kz5mvA==

% Router Certificate successfully imported

Manual(config)#
```

## Troubleshooting

### SCEP trustpoint connection issues

The only real issue I ran into on this lab was the CA was unreachable due to a missing static route. 

```
SCEP(config)#crypto pki authenticate CERT_TP
% Error in receiving Certificate Authority certificate: status = FAIL, cert length = 0

SCEP(config)#
*Dec 30 07:16:20.644: %PKI-3-SOCKETSEND: Failed to send out message to CA server.
SCEP(config)#
SCEP(config)#do ping 10.0.0.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.0.0.1, timeout is 2 seconds:
.....
Success rate is 0 percent (0/5)
SCEP(config)#ip route 10.0.0.1 255.255.255.255 192.168.1.1
SCEP(config)#do ping 10.0.0.1                             
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 10.0.0.1, timeout is 2 seconds:
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 8/12/20 ms


```