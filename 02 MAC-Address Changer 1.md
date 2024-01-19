## 02 MAC-Address Changer: Part 1

### What is a MAC-Address?
MAC-Address Introduction
* MAC = __Media Access Control__
* it is
    * __permament, physical,__ and __unique__
    * assigned to a decive by the manufacturer
* in networks,
    * used to identify devices and transfer data between them
    * data goes from source-MAC to destination-MAC
* implications of changing it
    * create anonymity & obscurity
    * circumvent filters & access systems
    * create evil-twin (impersonate another device)

Finding & Changing the MAC-Address
* to _find MAC-Addresses_, run `ifconfig` in terminal
    ```shell
    $ ifconfig
    eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 192.168.238.128  netmask 255.255.255.0  broadcast 192.168.238.255
            inet6 fe80::20c:29ff:fe52:5f12  prefixlen 64  scopeid 0x20<link>
            ether 00:0c:29:52:5f:12  txqueuelen 1000  (Ethernet)
            [...]
    ```
* this will display `eth0`, `l0` and maybe `wlan0` interfaces
    * `inet`: IPv4-address
    * `inet6`: IPv6-address
    * `ehter`: MAC-Address
* to change MAC-Addresses_, run following steps
    * `ifconfig eth0 down` to disable the interface (no response means success)
    * `ifconfig eth0 hw ether 00:11:22:33:44:55` to change the address
    * `ifconfig eth0 up` to enable the interface
    * `ifconfig` to see results
    ```shell
    $ ifconfig             
    eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
            inet 192.168.238.129  netmask 255.255.255.0  broadcast 192.168.238.255
            inet6 fe80::211:22ff:fe33:4455  prefixlen 64  scopeid 0x20<link>
            ether 00:11:22:33:44:55  txqueuelen 1000  (Ethernet)
            [...]
    ```

### Running Linux Commands with Python
Subprocess Module
* Python's `subprocess` module can execute system commands
    * see [documentation](https://docs.python.org/3/library/subprocess.html) for more details
* commands depend on the OS which runs the Python script
* most basic function is `call()` to run terminal commands
    ```python
    import subprocess
    subprocess.call("COMMAND", shell=True)
    ```
    * the command is a string-argument, e.g. `"ifconfig"`

### Implementing a Simple MAC-Address Changer
```python
#!/usr/bin/env python3
import subprocess

# declare commands
down_cmd = "ifconfig eth0 down"
change_cmd = "ifconfig eth0 hw ether 00:11:22:33:44:66"
up_cmd = "ifconfig eth0 up"
show_cmd = "ifconfig"

# run commands
subprocess.call(down_cmd, shell=True)
subprocess.call(change_cmd, shell=True)
subprocess.call(up_cmd, shell=True)
subprocess.call(show_cmd, shell=True)
```
* run in terminal with `sudo python3 mac_changer.py`

### Parametrizing your Script
* we can using variables to parametrize the interface and MAC-address
    * default variables are capitalized and put on top of script
* this makes it easier to change the interface in one place instead of all over the code
* to put one string variable inside another string, we can used f-strings and curly braces `{}`
    ```python
    # declare defaults
    INTERFACE = "eth0"
    MAC_ADDRESS = "00:11:22:33:44:66"

    # declare commands
    down_cmd = f"ifconfig {INTERFACE} down"
    change_cmd = f"ifconfig {INTERFACE} hw ether {MAC_ADDRESS}"
    up_cmd = f"ifconfig {INTERFACE} up"
    ```

### Taking User Input through the Command Line
User Input
* Python has a built-in `input()` function that can collect user input through the terminal, BUT
    * cleaning this input can be messy
    * handling this input can disrupt the script
* therefore, we'll design our script like other CLI tools with flags
* Python also comes with an `argparse` module to facilitate this ([documentation](https://docs.python.org/3/library/argparse.html))

Python CLI with Argparser
* we want to add flags for specifying an interface and for a new MAC address 
    ```python
    # create argparser
    parser = argparse.ArgumentParser(description="CLI script to accept interface and MAC address")
    parser.add_argument("-i", "--interface", default=INTERFACE, help="Specify the network interface")
    parser.add_argument("-m", "--mac-address", default=MAC_ADDRESS, help="Specify the MAC address")
    ```
* wrap the code into function called `main()`
* at the bottom of the script, add the following code
    ```python
    if __name__ == "__main__":
        main()
    ```
    * this is good practice for a Python CLI script
* now our Python mac_changer.py can display a help message and accept user inputs

### Validating User Input
* the MAC address has fixed format
    * it consists of 12 digits optionally with characters
    * more truthfully, they are 6 so-called hexadecimal digits
    * separation can be done by colon `:` or dash `-`
* we can use the built-in Pyhton module `re` or regular expressions to validate this fixed pattern
    ```python
    import re

    def validate_mac_address(mac_address: str) -> bool:
        # regex pattern for validating MAC address
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'

        # check if the MAC address matches the pattern
        if re.match(pattern, mac_address):
            return True
        else:
            return False
    ``` 