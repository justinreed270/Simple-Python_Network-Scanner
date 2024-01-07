import socket

def scan_port(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((host, port))
    if result == 0:
        print(f"Port {port} is open")
    sock.close()

def main():
    host = input("Enter the IP address or hostname: ")
    start_port = int(input("Enter the starting port: "))
    end_port = int(input("Enter the ending port: "))
    for port in range(start_port, end_port + 1):
        scan_port(host, port)

if __name__ == "__main__":
    main()
