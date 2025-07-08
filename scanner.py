import socket
import threading
import json
import argparse
import os
import datetime
import logging
import multiprocessing

# Setup log
logging.basicConfig(
    filename="scan.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

open_ports = []
lock = threading.Lock()

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                with lock:
                    open_ports.append({"port": port, "protocol": "TCP"})
                    logging.info(f"TCP port {port} is open")
    except Exception as e:
        logging.error(f"Error scanning TCP port {port}: {e}")

def scan_udp(ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(timeout)
            s.sendto(b"", (ip, port))
            s.recvfrom(1024)
            with lock:
                open_ports.append({"port": port, "protocol": "UDP"})
                logging.info(f"UDP port {port} is open or responded")
    except socket.timeout:
        pass  # Silenzio: porta probabilmente filtrata
    except Exception as e:
        logging.error(f"Error scanning UDP port {port}: {e}")

def genera_report_html(result):
    html = f"""<html>
<head>
    <title>Scan Report for {result['target']}</title>
    <style>
        body {{ font-family: Arial; background: #f4f4f4; color: #333; padding: 20px; }}
        h1 {{ color: #005a9c; }}
        table {{ border-collapse: collapse; width: 50%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
        th {{ background-color: #eee; }}
    </style>
</head>
<body>
    <h1>Scan Report for {result['target']}</h1>
    <table>
        <tr><th>Port</th><th>Protocol</th></tr>"""
    for port_info in result["open_ports"]:
        html += f"<tr><td>{port_info['port']}</td><td>{port_info['protocol']}</td></tr>"
    html += """
    </table>
</body>
</html>"""
    with open("report.html", "w") as f:
        f.write(html)

def main():
    parser = argparse.ArgumentParser(description="Advanced Port Scanner v2.0")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument('--udp', action='store_true', help='Esegui anche scansione UDP')
    args = parser.parse_args()

    max_threads = multiprocessing.cpu_count() * 5  # dinamico
    sem = threading.Semaphore(max_threads)

    threads = []

    for port in range(args.start, args.end + 1):
        sem.acquire()
        t = threading.Thread(target=lambda p=port: (scan_port(args.ip, p), sem.release()))
        threads.append(t)
        t.start()

    if args.udp:
        for port in range(args.start, args.end + 1):
            sem.acquire()
            t = threading.Thread(target=lambda p=port: (scan_udp(args.ip, p), sem.release()))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    result = {
        "target": args.ip,
        "open_ports": sorted(open_ports, key=lambda x: x['port'])
    }

    with open("open_ports.json", "w") as f:
        json.dump(result, f, indent=4)

    genera_report_html(result)
    print("✅ Scan completo. Risultati salvati in open_ports.json e report.html")

if __name__ == "__main__":
    main()

