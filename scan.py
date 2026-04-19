import socket
import threading

def run_scan(target_IP, mode, ports_input=None, first_port=None, last_port=None):

    output = ""   # ✅ FIX 1 (must be here)

    file = open("scan_results.txt", "a", encoding="utf-8")
    lock = threading.Lock()

    common_ports = {
        1: "ftp",
        22: "ssh",
        25: "smtp",
        53: "dns",
        80: "http",
        443: "https",
        3306: "mysql",
        8080: "http-alt",
        5357: "wsdapi",
        135: "msrpc",
        139: "netbios-ssn",
        8009: "ajp13",
        445: "microsoft-ds"
    }

    file.write("\n===== NEW SCAN =====\n")
    file.write(f"Target: {target_IP}\n")

    open_ports = 0
    total_ports = 0
    results = []
    closed_ports = []

    semaphore = threading.Semaphore(50)

    def scan_port(port):
        nonlocal open_ports, total_ports  # ✅ FIX

        with semaphore:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            total_ports += 1
            result = s.connect_ex((target_IP, port))

            if result == 0:
                open_ports += 1

                if port in common_ports:
                    service = common_ports[port]
                else:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "unknown"

                with lock:
                    results.append((port, service))

            else:
                with lock:
                    closed_ports.append(port)

            s.close()

    # ================= MODE 1 =================
    if mode == "1":
        try:
            ports = ports_input.split(",")  # ✅ FIX
        except:
            return "Invalid ports format"

        output += "Checking if host is up...\n"

        host_up = False

        for port in ports:
            port = int(port)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            if s.connect_ex((target_IP, port)) == 0:
                host_up = True
                s.close()
                break
            s.close()

        if host_up:
            output += "Host is up\n"
        else:
            output += "Host may be down or ports closed\n"
            return output

        output += "\nStarting port scan...\n"

        threads = []
        for port in ports:
            port = int(port)
            t = threading.Thread(target=scan_port, args=(port,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    # ================= MODE 2 =================
    elif mode == "2":

        output += "Checking if host is up...\n"

        host_up = False

        for port in range(first_port, last_port + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)

            if s.connect_ex((target_IP, port)) == 0:
                host_up = True
                s.close()
                break

            s.close()

        if host_up:
            output += "Host is up\n"
        else:
            output += "Host may be down or ports closed\n"
            return output

        output += "\nStarting port scan...\n"

        threads = []
        for port in range(first_port, last_port + 1):
            t = threading.Thread(target=scan_port, args=(port,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    # ================= OUTPUT =================
    results = list(set(results))
    results.sort()

    output += "\nPORT     STATE SERVICE\n"

    for port, service in results:
        line = f"{str(port)+'/tcp':<10} open  {service}"
        output += line + "\n"
        file.write(line + "\n")

    output += f"\nPorts scanned: {total_ports}\n"
    output += f"\nOpen ports: {open_ports}\n"
    output += "\nScan done.\n"

    file.close()

    return output
