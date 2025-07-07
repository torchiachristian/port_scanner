import socket
import threading
import json
import argparse

open_ports = []

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="End port (default: 1024)")
    args = parser.parse_args()

    threads = []

    for port in range(args.start, args.end + 1):
        t = threading.Thread(target=scan_port, args=(args.ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    result = {
        "target": args.ip,
        "open_ports": sorted(open_ports)
    }

    with open("open_ports.json", "w") as f:
        json.dump(result, f, indent=4)

    print("Scan completo. Risultati salvati in open_ports.json")

if __name__ == "__main__":
    main()
