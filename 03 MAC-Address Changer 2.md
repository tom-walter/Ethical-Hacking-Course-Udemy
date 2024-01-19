## 03 MAC-Address Changer: Part 2

### What is an algorithm?
Algortihm Design and Testing
* an algorithm performs a number of steps to solve a problem
* an algroithm breaks down a problem into a set of smaller problems that can be solved step-by-step
* to know if an algorithm succeeded, it is good practice to write tests
* a test hands an input to the algorithm and checks if it produces the expected output/result for that input   


MAC-Changer Algorithm Steps
* the MAC-Changer runs in a loop:
1. Run and read `ifconfig`
2. Save MAC address from output
3. Check if MAC address is already equal to user request
4. If not, validate user input and change MAC address

Step 1: Run and read `ifconfig`
* use `subprocess.check_output("command")`
* this executes the given command and returns the output as string
* from there, we need to filter the current MAC address

Step 2: Save MAC address from output
* use Python's regex to filter for the MAC address
    * you can use https://pythex.org/ to built a filter
* understanding the MAC address and building a pattern
    * starts with `ether`
    * separated with one whitespace `\s+`
    * hexadecimal numbers consist of digits `0-9` and letters `a-f` or `A-F`
    * they are separated by colon `:` or dash `-`
    * this combines into regex
    ```python
    r"ether\s+([0-9a-fA-F:]{17})"
    ```

Steps 3 & 4 are already implemented from last time.

### Keeping Records of MAC Address Changes
* when repeatedly changing your MAC addresses, it is good practice to keep a record of these changes (just in case you want to recover an old mac address)
* we can create a simple log file that tracks the datetime, interface, old and new MAC address each time we change it
* create a new file called `mac_history.csv` and enter this `datetime,interface,old_mac,new_mac` as first line
    * CSV stands for comma-separated value
    * but the separater can be chosen by you and MUST be consistent for the entire document
* using Python's built-in `datetime` library, we can get the time when the change occured
    ```python
    from datetime import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ``` 
* with Python's `pathlib` library, we can create file and navigate the filesystem as well as read, write and append files
* implement the logging function and run it after the MAC address was successfully changed
    ```python
    def log_mac_change(interface: str, old_mac: str, new_mac: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp},{interface},{old_mac},{new_mac}\n"
        log_file_path = Path("mac_history.csv")

        # Append the log entry to the CSV file
        with log_file_path.open(mode="a") as file:
            file.write(log_entry)
    ```