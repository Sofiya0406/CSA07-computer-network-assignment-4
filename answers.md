# CO4 Assignment 4 – Designing Network Topologies

**Student:** S. Sofiya  
**Register Number:** 192521248  
**Department:** Information Technology  
**Course:** CSA07 – Computer Networks

> Assumptions are stated wherever the question does not provide a device speed, AP capacity, exact floor plan or equipment price. Replace estimates with measured values from your own Packet Tracer simulation where required.

---

## TASK 1 – Why Does the Whole Office Stop?

### 1.1 Explain each complaint

1. **Moving one desk disconnects everyone:** A bus network uses one shared backbone cable. A break, loose connector or incorrect termination can interrupt the whole segment.
2. **Server file saving takes a minute:** All 30 computers share the same collision domain and the hub repeats traffic to every port. Collisions and shared bandwidth reduce useful throughput, especially during month-end.
3. **Internet stops when the router restarts:** The single home router is the only internet gateway. It is a single point of failure.

Other weaknesses:
- Hub-based Ethernet is half-duplex and has one collision domain.
- No easy expansion or fault isolation; one cable fault can affect many users.
- The home router may lack business-grade firewall, logging, VLAN and capacity features.
- A long bus cable is difficult to troubleshoot and physically protect.

### 1.2 Redesign as an extended star

**Logical topology**

```text
                  Internet
                     |
              Business Firewall
                     |
               Edge Router
                     |
             Core L3 Switch
               /         \
       Floor-1 Switch   Floor-2 Switch
        /   |   \        /   |   \
      PCs  Server Printer PCs  PCs  AP
```

**Physical topology:** Install a locked network rack in the equipment room. Run separate Cat6/Cat6A horizontal cables from each desk to the nearest floor access switch. Connect each floor switch to the core switch using fibre (or a suitable high-speed uplink). Connect the server and printer to dedicated switch ports. Label both ends of every cable and use patch panels.

**Bandwidth calculation (illustrative):**
- Existing shared 10 Mbps coax Ethernet assumption: `10 / 30 = 0.333 Mbps` average share per computer under equal simultaneous demand. Actual throughput is lower with collisions and protocol overhead.
- New design assumption: 1 Gbps full-duplex access port per PC and a 10 Gbps server/core path. Each PC has a dedicated 1 Gbps link; 30 users share the 10 Gbps server path, giving a theoretical equal share of `10,000 / 30 = 333.3 Mbps` per user when all are transferring simultaneously. Real throughput depends on server, storage and traffic.

### 1.3 Defence (under 100 words)

The extended-star design removes the shared coax backbone and hub. A desk cable fault now normally affects only that desk. Switches provide dedicated full-duplex access links and reduce collisions, improving server transfers. A business router and firewall replace the home router and provide stronger security and traffic control. The core and floor switches make expansion and troubleshooting easier. Redundant gateway or internet links can further reduce the internet single point of failure.

### Alternative: all-wireless Wi-Fi 6 versus switched star

If one Wi-Fi 6 AP provides an illustrative 1.2 Gbps aggregate PHY rate, an equal theoretical share for 30 active users is `1,200 / 30 = 40 Mbps` before wireless overhead, interference and retransmissions. A switched star gives each wired PC a dedicated 1 Gbps access link and a 10 Gbps server path in this design. For large month-end file transfers, wired switched Ethernet is more predictable and reliable. Wi-Fi 6 is useful for mobile devices, not as the only connection for all office PCs.

---

## TASK 2 – How Many Links Can the Hospital Afford?

### 2.1 Link, port and cost calculations

There are five blocks. For this calculation, a bus is represented as four backbone segments joining five blocks in a line. Each fibre link uses two switch ports. Cost per link is:

`Fibre run ₹60,000 + 2 × switch port ₹18,000 = ₹96,000`

| Topology | Links | Fibre switch ports | Cost |
|---|---:|---:|---:|
| Bus | 4 | 8 | ₹3,84,000 |
| Ring | 5 | 10 | ₹4,80,000 |
| Star (data centre at centre) | 4 | 8 | ₹3,84,000 |
| Full mesh | 10 | 20 | ₹9,60,000 |

Port count is the total number of link-end ports. A central star switch needs four block-facing ports; each block needs one uplink port.

### 2.2 Single cable failure

- **Bus:** Cutting any backbone segment separates the blocks on one side from the blocks on the other side. It can disconnect emergency or theatres depending on the cut location.
- **Ring:** One cable cut does not disconnect the blocks because traffic can travel the other way around the ring. Two suitably placed cuts can isolate a block or a section.
- **Star:** Cutting the emergency-to-centre link disconnects emergency; cutting the theatre-to-centre link disconnects theatres. A central switch failure can disconnect all blocks.
- **Full mesh:** One cable cut does not disconnect any block because alternate paths remain.

### 2.3 Least-cost reliable hybrid design

**Assumption:** The patient-record server is located in the administration block, and the five named blocks are the five core sites. Use a **five-link fibre ring as a sparse/partial-mesh core**, with a star of access switches and endpoints inside each block. The ring gives two directions between every pair of blocks, so one core cable cut does not isolate emergency or operation theatres from the administration/server block.

- Core ring links: `5`
- Link-end switch ports: `5 × 2 = 10`
- Fibre and port cost per link: `₹60,000 + (2 × ₹18,000) = ₹96,000`
- Total cost: `5 × ₹96,000 = ₹4,80,000`

This is the least-cost simple single-link-resilient design among the listed basic options: a bus and a star fail the single-cut rule, while a full mesh costs ₹9,60,000. Use managed switches and a loop-prevention/ring-recovery mechanism (or routed links with a dynamic routing protocol) so the alternate path becomes active after a cut. A ring does not survive every pair of cable cuts; two cuts can isolate a section. If the requirement also includes a core-switch failure, add node-level redundancy/dual core switches and recalculate the cost.

### 2.4 Simulation procedure

1. Add five block switches in Packet Tracer and connect them in a fibre ring.
2. Place the patient-record server in the administration block; connect emergency and theatres to their local block switches.
3. Configure the ring using a supported Layer-2 loop-prevention design or routed links.
4. Verify pings from emergency and theatres to the patient-record server.
5. Shut down one ring link and repeat the pings after the network reconverges.
6. Capture the topology, interface status and successful ping output.

### Completed Python code

The completed breadth-first search program is in `Task02/topology_failure.py`. It models the four graph types and tests connectivity after each single-link failure. For the assignment's supplied code, the expected output for `n = 6` is:

```text
bus   links 5  ... single-link failures survived 0/5
ring  links 6  ... single-link failures survived 6/6
star  links 6  ... single-link failures survived 0/6
mesh  links 15 ... single-link failures survived 15/15
```

The script prints the full output when run.

### Alternative: five-block fibre ring

A ring has 5 links, 10 ports and costs `5 × ₹96,000 = ₹4,80,000`. It survives any one link cut. It does not guarantee survival of every pair of cuts: two cuts can isolate the blocks lying between the failed links. The dual-homed hybrid is more targeted because emergency, theatres and the patient-record server have independent paths, but its final cost depends on the number of dual-homed endpoints and core equipment.

---

## TASK 3 – Devices, Media and Cabling

### 3.1 Check the cabling plan

TIA/EIA structured copper cabling limits are 90 m for the permanent link and 100 m for the complete channel (including patch cords).

| Run | Given length | Finding | Recommendation |
|---|---:|---|---|
| Consulting rooms | 35–80 m | Within 90 m permanent-link limit | Cat6 UTP is acceptable for 1 Gbps; use Cat6A if 10 Gbps/future capacity is required |
| Pharmacy | 96 m | Exceeds 90 m permanent link; may fit 100 m channel only if patch cords keep total at or below 100 m | Move/ add a telecom room or use fibre; do not treat 96 m as a compliant permanent link |
| Waiting-hall APs | 60 m | Within limit | Cat6/Cat6A; consider Cat6A for Wi-Fi 6/6E AP uplinks and PoE |
| Main-building link | 420 m | Far beyond copper Ethernet channel limit | Fibre; multimode for suitable campus distances/data rates or single-mode for longer distance/future-proofing |

**Mixed T568A/T568B patch cable:** One end A and the other B makes a crossover cable. Older devices may need a crossover cable for like-device connections. Auto-MDIX on many modern switches/NICs detects and corrects pair direction, so the link may still work. Use the same standard at both ends (straight-through) for structured cabling and consistency.

### 3.2 Device selection and domains

- **Layer-2 access switches:** connect PCs, printers, cameras and APs; each switch port is its own collision domain.
- **Layer-3 switch:** performs inter-VLAN routing between hospital VLANs.
- **Router:** connects the hospital to external WAN/ISP networks.
- **Wireless access points:** connect Wi-Fi clients and map SSIDs to VLANs.
- **Firewall:** filters traffic between internal zones and the internet.
- **Hub:** do not use; it creates one shared collision domain and repeats traffic.

**Domain count (example):** With 24 active switched access ports, there are 24 collision domains. If the outpatient block has four VLANs (clinical, staff, guest and CCTV), there are four broadcast domains in that block, assuming each VLAN is one Layer-2 broadcast domain and no additional subnet/VLAN split.

### 3.3 Bill of materials – outpatient block

Illustrative estimate based on 24 wired endpoints, 4 APs, one 48-port PoE access switch and one fibre uplink.

| Item | Quantity | Notes |
|---|---:|---|
| 48-port PoE+ Layer-2 switch | 1 | 24 endpoints + 4 APs + spare ports |
| Layer-3 core switch ports | 2 | One active uplink plus one spare/redundant uplink, if supported |
| Cat6A horizontal cable | 1 lot | Measure actual routes; add 10% spare |
| Fibre uplink cable | 420 m route | Main-building run; order `420 × 1.10 = 462 m` |
| Fibre transceivers | 2 | Match fibre type and switch optics |
| Patch panel, 24/48-port | 1 | Rack termination |
| RJ45 keystone jacks | 28 | 24 wired endpoints + 4 APs, plus spares as needed |
| Patch cords | 28 or more | Rack and endpoint patching |
| Rack with cable management | 1 | Size to equipment and growth |
| UPS | 1 | Size from measured switch and PoE load |
| Labels and cable accessories | 1 lot | Labels, ties, faceplates, conduits |

The exact horizontal-cable quantity cannot be calculated from the given information because individual room routes and endpoint counts are not fully specified. Measure each route and apply 10% spare.

### 3.4 T568B colour order

Pin 1 to pin 8:
1. White-orange
2. Orange
3. White-green
4. Blue
5. White-blue
6. Green
7. White-brown
8. Brown

Use T568B at both ends for a straight-through cable. Test with a cable tester and save a photo/result as practical evidence.

### Alternative: 420 m multimode fibre versus Cat6A plus mid-span switch

- **Multimode fibre:** supports hundreds of metres depending on fibre grade and Ethernet speed; 420 m may be within some OM4 10-GbE reach specifications but verify the exact optic standard. It is electrically non-conductive and immune to electromagnetic interference/lightning-induced ground potential differences.
- **Cat6A:** Ethernet copper channel is limited to 100 m. A switch halfway would still leave two copper segments; 420 m needs multiple powered intermediate switches and protected locations, not just one switch. Each adds power, UPS, maintenance and failure points.
- **Decision:** use fibre for the 420 m inter-building link. Select single-mode if future distance/speed flexibility is the priority; use multimode only after confirming optic reach and budget.

---

## TASK 4 – Shared Media, WLAN and WAN

### 4.1 Multiple access

**Pure ALOHA maximum throughput**

`Smax = 1 / (2e) = 0.184` or **18.4%** of channel capacity.

**Slotted ALOHA maximum throughput**

`Smax = 1 / e = 0.368` or **36.8%** of channel capacity.

**CSMA/CD minimum frame size**

- Cable length = 2,500 m
- Signal speed = `2 × 10^8 m/s`
- One-way propagation delay = `2500 / (2 × 10^8) = 12.5 μs`
- Round-trip propagation delay = `25 μs`
- Minimum bits = `10 × 10^6 × 25 × 10^-6 = 250 bits`
- Minimum bytes = `250 / 8 = 31.25 bytes`

Thus the theoretical minimum is 31.25 bytes under the stated assumptions. Ethernet's standard minimum frame size is 64 bytes, which exceeds this value. Switched full-duplex Ethernet has dedicated point-to-point transmit/receive paths, so collisions do not occur and CSMA/CD is unnecessary. Wi-Fi is a shared radio medium; stations use CSMA/CA to avoid collisions because they cannot reliably detect a collision while transmitting.

### 4.2 Wireless LAN plan for 300 phones

Illustrative design: deploy **6 managed Wi-Fi 6 access points**, about 50 associated phones per AP, after a site survey and capacity validation. Use wired PoE backhaul and place APs to limit co-channel interference.

- **2.4 GHz:** use only channels 1, 6 and 11 at 20 MHz width; reuse them in a non-adjacent pattern (for example AP1=1, AP2=6, AP3=11, AP4=1, AP5=6, AP6=11), with physical separation between APs using the same channel.
- **5 GHz:** use distinct non-overlapping 20/40 MHz channels selected from the locally permitted channel plan after checking DFS rules and neighbouring networks. Avoid assigning the same channel to adjacent APs.
- **Wi-Fi 6 OFDMA:** divides a channel into resource units so multiple clients can be served efficiently.
- **MU-MIMO:** allows an AP to communicate with multiple clients using multiple spatial streams.
- **BSS colouring:** helps devices distinguish their own BSS transmissions from neighbouring BSS traffic and can improve spatial reuse.
- **Bluetooth:** suitable for short-range, low-data-rate peripherals such as approved patient-monitoring accessories. Do not use it as the main network for high-bandwidth imaging, critical alarms without validated clinical design, or devices requiring guaranteed low latency/reliability.

### 4.3 Backbone and WAN

**ATM overhead**

- ATM cell = 53 bytes
- Header = 5 bytes
- Payload = 48 bytes
- Header overhead as a fraction of total cell = `5 / 53 × 100 = 9.43%`
- Payload efficiency = `48 / 53 × 100 = 90.57%`

**Ethernet comparison:** A basic Ethernet frame has a 14-byte header and 4-byte FCS. For a 1,500-byte payload, frame size is 1,518 bytes, so header+FCS overhead is `18 / 1518 × 100 ≈ 1.19%` (not counting preamble and inter-frame gap). Ethernet therefore has lower framing overhead for large frames.

**Virtual-circuit identifiers**
- Frame Relay: DLCI (Data-Link Connection Identifier)
- ATM: VPI/VCI (Virtual Path Identifier / Virtual Channel Identifier)
- MPLS: label in the packet's label stack

**Three branch clinics:** Choose an internet VPN for a limited budget when encrypted connectivity is required and the clinics can tolerate best-effort internet performance. Choose managed MPLS when the provider's SLA, predictable QoS and traffic prioritisation justify the higher recurring cost. For video consultations, prioritise real-time traffic using QoS at the clinic edge; an internet VPN alone does not guarantee bandwidth or delay.

### Alternative: VPN versus MPLS

An ordinary internet VPN generally provides encryption but no end-to-end bandwidth or delay guarantee; performance depends on ISP congestion and the public internet. Managed MPLS can offer contracted bandwidth, latency/jitter targets and provider QoS, depending on the service SLA. I would accept a higher MPLS monthly cost only if the SLA specifies measurable availability, latency, jitter, packet loss and repair time, and the clinical video workload needs those guarantees. The assignment gives no provider prices, so an exact monthly cost difference cannot be calculated.

---

## TASK 5 – Separate the Guests from the Office

### 5.1 VLAN configuration

802.1Q inserts a **4-byte VLAN tag** into an Ethernet frame.

Completed access-switch configuration is in `Task05/SW-Admin.txt`. Main commands:

```text
vlan 30
 name Guest-WiFi
interface range FastEthernet0/13 - 20
 switchport mode access
 switchport access vlan 20
interface range FastEthernet0/21 - 24
 switchport mode access
 switchport access vlan 30
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
```

### 5.2 Inter-VLAN routing and guest ACL

Use router-on-a-stick or an L3 switch. Sample router subinterfaces and an ACL are in `Task05/Router-on-a-Stick.txt`. The guest VLAN is permitted to reach the internet-facing network but denied access to the office and CCTV private subnets. Apply the ACL in the correct direction and test it in Packet Tracer.

### 5.3 Proof and broadcast domains

Before VLANs: all devices on the same unsegmented Layer-2 LAN are in **one broadcast domain**. After VLANs 10, 20 and 30: there are **three broadcast domains**.

Expected tests:
- Office PC to another office PC: ping succeeds.
- Guest PC to office PC: ping fails.
- Guest PC to CCTV device: ping fails.
- Guest PC to internet test destination: succeeds only if routing/NAT and the ACL are configured.
- Office/admin PC to permitted CCTV management address: depends on the security policy configured.

Save `show vlan brief`, `show interfaces trunk`, routing/ACL outputs and ping screenshots.

### Alternative: separate physical guest switch and internet

A separate switch and ISP connection cost more hardware and a second service, but provide stronger physical separation and reduce the risk of VLAN/trunk misconfiguration. VLAN separation is cheaper and easier to manage centrally. Physical separation is worthwhile for high-security guest access, regulatory requirements, or when guest equipment must remain isolated even if the internal switching configuration is compromised.

---

## TASK 6 – Design Challenge: New University Campus

### Stage 1 – Estimate requirements

Illustrative planning assumptions (confirm with the university):
- Academic block: 800 users, 1,000 wired/wireless devices, peak aggregate 2 Gbps.
- Laboratories: 600 computers plus 100 staff/IoT devices; peak 3 Gbps.
- Library: 500 users, 600 devices; peak 1 Gbps.
- Hostels: 3,000 students, assume 2 devices each = 6,000 devices; peak 6 Gbps.
- Auditorium: 500 concurrent users/devices; peak 1 Gbps.
- Data centre: servers, storage, security and management; peak north-south/east-west capacity planned at 10 Gbps initially.

Testable requirements:
1. Every building must have wired and Wi-Fi coverage.
2. Student, staff, guest and CCTV traffic must be isolated in separate VLANs/subnets.
3. Critical core and internet connectivity must survive one link failure.
4. Two ISPs must be connected with automatic failover (and load sharing if supported).
5. Provide scalable addressing and spare switch ports/AP capacity for ten years.
6. Verify inter-VLAN policy, DHCP, DNS, internet access and failover with recorded tests.

### Stage 2 – Hierarchical hybrid topology

```text
                ISP-1             ISP-2
                  \                 /
                 Edge Router / Firewall Pair
                           |
                    CORE-A ===== CORE-B
                     ||  \       /  ||
                     ||   \     /   ||
                Distribution switches per building
                  /      |       |       \
             Academic  Labs   Library   Hostels
                                |          |
                            Auditorium  Access switches/APs
                           Data Centre dual-connected to core
```

Use a redundant partial-mesh core (CORE-A and CORE-B), dual uplinks from building distribution switches, and star topology from each access switch to end devices. Use fibre backbone between buildings; use Cat6A to desks/APs. Provide dual power/UPS for core and critical distribution equipment.

### Stage 3 – Devices, media and services

- Two Layer-3 core switches with redundant high-speed links.
- Redundant distribution switches for large buildings/labs/hostels.
- PoE+ access switches for APs, phones and cameras.
- Wi-Fi 6/6E APs after a predictive and on-site RF survey.
- Single-mode fibre between buildings; Cat6A horizontal cabling.
- Edge routers and next-generation firewalls for two ISP connections.
- VLANs: Student, Staff, Guest, CCTV, Labs, Servers and Network Management.
- DHCP scopes per VLAN; central DNS; ACLs/firewall rules between VLANs.
- Use dynamic routing (for example OSPF internally) and appropriate ISP failover (BGP if the organisation has its own public ASN/prefixes, otherwise provider-supported failover).

### Stage 4 – Sample address plan

Use private address space `10.20.0.0/16`. Example subnets are listed in `Task06/address-plan.csv`.

| VLAN | Purpose | Example subnet | Gateway |
|---:|---|---|---|
| 10 | Staff | 10.20.10.0/23 | 10.20.10.1 |
| 20 | Students | 10.20.20.0/20 | 10.20.20.1 |
| 30 | Guest Wi-Fi | 10.20.40.0/21 | 10.20.40.1 |
| 40 | CCTV | 10.20.50.0/23 | 10.20.50.1 |
| 50 | Laboratories | 10.20.60.0/22 | 10.20.60.1 |
| 60 | Servers | 10.20.70.0/24 | 10.20.70.1 |
| 99 | Network management | 10.20.99.0/24 | 10.20.99.1 |

**Oversubscription examples (assumptions):**
- Labs: 600 PCs at 100 Mbps access = 60 Gbps theoretical access capacity. Two 10 Gbps uplinks (20 Gbps aggregate) give 3:1 oversubscription.
- Hostel: assume 6,000 devices at an average busy-hour demand of 2 Mbps = 12 Gbps offered demand. Two 10 Gbps uplinks provide 20 Gbps; demand-to-uplink ratio = 0.6:1. Actual busy-hour usage must be measured.
- Academic: assume 1,000 devices at 100 Mbps access = 100 Gbps theoretical access; dual 10 Gbps uplinks = 5:1 oversubscription.

**Indicative bill of materials (quantities subject to site survey):**
- 2 core L3 switches with redundant power supplies
- 2 edge routers / firewall appliances (or HA firewall pair with dual ISP handoffs)
- 2 distribution switches per large building; 1 or more for smaller buildings
- Access switches sized by endpoint and PoE count (600 lab PCs need at least 13 × 48-port switches before spare capacity)
- Wi-Fi 6/6E APs sized by RF coverage and concurrent client capacity
- Single-mode fibre, optical transceivers, patch panels, racks, UPS, Cat6A, keystones and patch cords
- Monitoring, authentication and backup configuration system

### Stage 5 – Packet Tracer demonstration

Build a reduced topology with:
- Two core multilayer switches
- Two building distribution/access switches
- One router per ISP (or two simulated ISP routers)
- One server and at least two PCs in different VLANs
- Trunk links, SVIs or router-on-a-stick, DHCP and ACLs

Demonstrate:
1. Same-VLAN connectivity.
2. Permitted inter-VLAN connectivity.
3. Guest-to-staff and guest-to-CCTV traffic blocked.
4. Internet/ISP-1 connectivity.
5. Shut down one core link and show that the alternate path keeps critical connectivity.

Save the `.pkt` file, configurations, `show` command outputs and screenshots.

### Alternative: collapsed core

A collapsed core combines core and distribution functions and may save one pair of distribution switches or reduce equipment cost in a small campus. However, a single collapsed-core switch failure can disconnect all buildings, users, servers and both ISP paths if there is no independent redundant device. For a 40-acre campus with 600 lab PCs and 3,000 hostel students, the outage impact is high. A redundant pair of collapsed-core switches is safer, but it still concentrates more functions in fewer devices. The initial saving is not worth a campus-wide single point of failure over ten years; use a redundant hierarchical core.

---

## Final conclusion

A switched hierarchical design with structured cabling, fibre building backbones, VLAN segmentation, Layer-3 routing, firewall policies and redundant core/ISP paths is more reliable and scalable than a shared bus or hub-based network. Calculations support the topology and media choices; Packet Tracer execution and screenshots must be added as independent evidence.
