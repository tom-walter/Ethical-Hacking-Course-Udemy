import scapy.all as scapy
from argparse import ArgumentParser


def scan(ip):
    # create a basic ARP request
    arp_request = scapy.ARP(pdst=ip)

    # create a broadcast at all
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # combine
    arp_request_broadcast = broadcast / arp_request

    # send, capture answered and unanswered packets
    answered, unanswered = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)

    client_list = [{"ip": ans[1].psrc, "mac": ans[1].hwsrc} for ans in answered]
    return client_list

def print_results(client_list):
    print("IP Adress\t\tMAC Adress")
    print("-"*40)
    for client in client_list:
        print(f"{client['ip']}\t\t{client['mac']}")

def main():
    # create default
    ip_range = "192.168.238.1/24"

    # create argparser
    parser = ArgumentParser(
        description="CLI script to scan for local IP-addresses and their associated MAC"
        )
    parser.add_argument("-t", "--target", default=ip_range, help="specify the target IP or range")

    args = parser.parse_args()

    clients = scan(ip=args.target)
    print_results(client_list=clients)
    

    
if __name__ == "__main__":
    main()