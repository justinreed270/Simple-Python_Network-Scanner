# Simple-Python_Network-Scanner
 
# Python Network Scanner

This is a simple Python script that can be used to scan ports on a given IP address or hostname.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

- Python 3.x

## Setup Instructions:
1. Clone the repo
2. Download PsExec64.exe


## system level installs:
apt install samba-common-bin


## How to Use

1. Open a terminal or command prompt.
2. Clone the repository or download the script file.
3. Navigate to the directory where the script is located.
4. Run the following command to execute the script:
    
    ```bash
    python network_scanner.py
    
    ```
    
5. Enter the IP address or hostname you want to scan when prompted.
6. Enter the starting port number when prompted.
7. Enter the ending port number when prompted.
8. The script will scan the specified range of ports on the given IP address or hostname and display the open ports, if any.

## Example

Let's say you want to scan ports on the IP address "192.168.0.1" from port 1 to port 100. Here's how you would use the script:

1. Open a terminal or command prompt.
2. Navigate to the directory where the script is located.
3. Run the following command:
    
    ```bash
    python network_scanner.py
    
    ```
    
4. Enter "192.168.0.1" when prompted for the IP address or hostname.
5. Enter "1" when prompted for the starting port.
6. Enter "100" when prompted for the ending port.
7. The script will scan ports 1 to 100 on the IP address "192.168.0.1" and display the open ports, if any.

## Notes

- The script uses the `socket` module in Python to perform the port scanning.
- The script will only scan TCP ports.
- The timeout for each port scan is set to 1 second. You can modify this value in the `scan_port` function if needed.
