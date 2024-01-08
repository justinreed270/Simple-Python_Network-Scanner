import socket

def scan_port(host, port):
    """
    Function to scan a given port on a host.
    Args:
        host (str): IP address or hostname to scan.
        port (int): Port number to scan.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    if result == 0:
        print(f"Port {port} is open")
    sock.close()

def main():
    """
    Main function to execute the network scanner.
    """
    host = input("Enter the IP address or hostname: ")
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))
    for port in range(start_port, end_port + 1):
        scan_port(host, port)

if __name__ == "__main__":
    main()