import socket 
target_IP =int(input("entrer votre IP"))
for port in range(0,200):
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)