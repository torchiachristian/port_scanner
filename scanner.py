import socket
import threading
import json
import argparse
import os

open_ports = []
lock = threading.Lock()

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            with lock:
                open_ports.append({"port": port, "protocol": "TCP"})
        sock.close()
    except:
        pass

def scan_udp(ip, port, timeout=1):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        s.sendto(b"", (ip, port))
        s.recvfrom(1024)
        with lock:
            open_ports.append({"port": port, "protocol": "UDP"})
    except socket.timeout:
        pass
    except:
        pass
    finally:
        s.close()

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
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("--end", type=int, default=1024, help="End port (default: 1024)")
    parser.add_argument("--udp", action="store_true", help="Include UDP scan")
    args = parser.parse_args()

    threads = []

    max_threads = os.cpu_count() * 4

    for port in range(args.start, args.end + 1):
        while threading.active_count() >= max_threads:
            pass
        t = threading.Thread(target=scan_port, args=(args.ip, port))
        threads.append(t)
        t.start()

    if args.udp:
        for port in range(args.start, args.end + 1):
            while threading.active_count() >= max_threads:
                pass
            t = threading.Thread(target=scan_udp, args=(args.ip, port))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()

    result = {
        "target": args.ip,
        "open_ports": sorted(open_ports, key=lambda x: x["port"])
    }

    with open("open_ports.json", "w") as f:
        json.dump(result, f, indent=4)

    genera_report_html(result)
    print("Scan completo. Risultati salvati in open_ports.json e report.html")

if __name__ == "__main__":
    main()

