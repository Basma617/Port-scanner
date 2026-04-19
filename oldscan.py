#the slow code , comparasion between this one and the new version in time 
import socket # Python library for creating and managing TCP/IP network connections, sending data and receiving it 
import time
import threading# to avoid the sequential execution
# custom service mapping
common_ports = {
    21: "ftp",
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
    445: "microsoft-ds"
   
}
target_IP= input("Enter the target IP adress\n").strip()
 #validation of IP
try:
    socket.gethostbyname(target_IP)
except:
    print("Invalid IP or hostname")
    exit()
# total port is 65 535 port
mode = input("Choose scan mode(1 = specific ports, 2 = port range):\n")
timeout=1
start_time= time.time()
open_ports=0
total_ports=0
if mode == "1":
    ports = input("Enter ports seperated by commas\n")
    ports = ports.split(",")
    print("Starting port scan...\n")

    for port in ports:
        port = int(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target_IP, port))
        total_ports+=1
        if result ==0:
            open_ports+=1
            try:
                service= socket.getservbyport(port)#add service detection
            except:
                service=common_ports.get(port,"uncknown")
            #try:find service name except: if not found → write "unknown"
        
            print("Connexion successful ", port, "OPEN →", service)
        else :
            print("Connexion failed ,Port",port,"CLOSED or FILRED\n")
        s.close()
elif mode == "2":
    first_port=int(input("Enter the first port that you'd like to test\n"))
    last_port=int(input("Enter the last port that you'd lie to test\n"))
    print("Starting port scan...\n")
    for port in range(first_port, last_port + 1):
        total_ports+=1
    #now  we're crating the TCP socket 
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # The first socket is the library ,the second one is the function that create the socket
    #socket.AF_INET (Address Family Internet) IPv4
    #socket.SOCK_STREAM means that the communicaton is going to use TCP
        s.settimeout(timeout)
        result=s.connect_ex((target_IP,port))
    #This is a predefined function of the Python socket object.
    # it returns 0->connection successful → port is open,  other->connection failed → port is closed or filtered
        if result == 0:
            open_ports += 1
            try:
                service= socket.getservbyport(port)#add service detection
            except:
                service= common_ports.get( port,"unknown")
            #try:find service name except: if not found → write "unknown"
            print("Connexion successful ", port, "OPEN →", service)
        else:
            print("Connexion failed ,Port",port,"CLOSED or FILRED\n")
        s.close()
end_time=time.time()
duration=end_time-start_time
print("Scan finished.\n")
print("Ports scanned:", total_ports)
print("Open ports:", open_ports)
print("Time:", round(duration, 2), "seconds")
print("Finish")