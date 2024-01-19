#!/usr/bin/env python3
import subprocess
from argparse import ArgumentParser, Namespace
import re
from datetime import datetime
from pathlib import Path 

# declare defaults
INTERFACE = "eth0"
MAC_ADDRESS = "00:11:22:33:55:77"

def validate_mac_address(mac_address: str) -> bool:
    # regex pattern for validating MAC address
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'

    # check if the MAC address matches the pattern
    if re.match(pattern, mac_address):
        return True
    else:
        return False

def get_mac_address(interface: str) -> str:
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    # parse the result if regex
    current_mac_address = re.search(r"ether\s+([0-9a-fA-F:]{17})", ifconfig_result)
    return current_mac_address.group(1)

def change_mac_address(parsed_args: Namespace) -> None:
    # declare commands
    down_cmd = f"ifconfig {parsed_args.interface} down"
    change_cmd = f"ifconfig {parsed_args.interface} hw ether {parsed_args.mac_address}"
    up_cmd = f"ifconfig {parsed_args.interface} up"
    show_cmd = ["ifconfig", parsed_args.interface]

    # run commands
    subprocess.call(down_cmd, shell=True)
    subprocess.call(change_cmd, shell=True)
    subprocess.call(up_cmd, shell=True)
    subprocess.call(show_cmd)
    
def log_mac_change(interface: str, old_mac: str, new_mac: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp},{interface},{old_mac},{new_mac}\n"
    log_file_path = Path("mac_history.csv")

    # Append the log entry to the CSV file
    with log_file_path.open(mode="a") as file:
        file.write(log_entry)

def main():
    # create argparser
    parser = ArgumentParser(description="CLI script to accept interface and MAC address")
    parser.add_argument("-i", "--interface", default=INTERFACE, help="Specify the network interface")
    parser.add_argument("-m", "--mac-address", default=MAC_ADDRESS, help="Specify the MAC address")

    args = parser.parse_args()
    
    # validate mac address
    if not validate_mac_address(args.mac_address):
        print(f"Invalid MAC address {args.mac_address}. Using default = {MAC_ADDRESS}")
        args.mac_address = MAC_ADDRESS

    # check current mac address
    old_mac_address = get_mac_address(args.interface)
    if old_mac_address == args.mac_address:
        print(f"Current MAC address is already requested MAC address: {args.mac_address}")
        return None
    else:
        # change the mac address
        print(f"Changing MAC address from {old_mac_address} to {args.mac_address}\n")
        change_mac_address(args)

        current_mac_address = get_mac_address(args.interface)
        if current_mac_address == args.mac_address:
            log_mac_change(args.interface, old_mac_address, args.mac_address)
            print("Successfully changed!")
        else:
            print("Change failed somehow.")


if __name__ == "__main__":
    main()