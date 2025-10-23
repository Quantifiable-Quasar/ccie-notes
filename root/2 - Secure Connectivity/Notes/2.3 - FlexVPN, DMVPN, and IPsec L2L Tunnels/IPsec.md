# IPsec
## Modes

\*dont really like the name of this section, but idk what to call it

**Tunnel:** Encapsulates packet in entirely new header (encrypt everything)

<figure class="image"><img style="aspect-ratio:538/392;" src="1_IPsec_image.png" width="538" height="392"></figure>

**Transport:** Encrypts only payload and shoves ESP header in existing headers  
\- used primarily for peer-to-peer connections

<figure class="image"><img style="aspect-ratio:548/388;" src="2_IPsec_image.png" width="548" height="388"></figure>

**ESP** is pretty much the only option used for IPsec (AH exists but no one should be using it)

*   port 50
*   Everything behind ESP header is encrypted
*   All that and the ESP header are authenticated
*   [RFC 4303](https://datatracker.ietf.org/doc/html/rfc4303)
*   Anti-Replay through sequence numbers+auth**:**

### **ISAKMP/IKE**

<a class="reference-link" href="IKE%20Deep%20Dive%20-%20WIP.md">IKE Deep Dive - WIP</a> - Notes on IKE

There's ISAKMP which is commonly associated with IKEv1 and there is also IKEv2. Do not use v1.

IKEv1 has main and aggressive mode. most implementations use aggressive mode

<figure class="image"><img style="aspect-ratio:553/343;" src="IPsec_image.png" width="553" height="343"></figure>

### Implementation

All this stuff is configured in the IPsec Profile. That controls IKE phase 2 SA paramaters.

Most implementations of IPsec are VTI based. Crypto maps can exist, but the VTI is the way to go.

There are implementation topolgies

**Site-to-Site:**

*   Full Mesh
*   Hub-and-Spoke
*   DMVPN
*   Static VTI
*   GET VPN

**Remote Access:**

*   Easy VPN
*   DVTI

## Resources

- [ ] CCIE Professional Development Series Network Security Technologies and Solutions Ch 15
- [x] Integrated Security Technologies and Solutions - Volume II
- [ ]