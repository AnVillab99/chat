
# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
import os

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port))

f =open("public.pem", "rb")

print("//////////////////////////////////////")
filesize = os.path.getsize("public.pem")
print(filesize)
print(str(filesize))
server.send(str(filesize).encode())
for i in range (filesize//2048):
    
    
    bytes_read = f.read(2048)
    if not bytes_read:
            break
    server.sendall(bytes_read)

print("#################")
# close the socket

# def encrypt(message):
#     f = open("public.pem", "r")
#     public = RSA.import_key(f.read())
#     # public (n,e)
    
#     cipher = PKCS1_OAEP.new(key=public)
#     cipher_text = cipher.encrypt(bytes(message, encoding="utf-8"))
#     print(cipher_text)

while True: 

    # maintains a list of possible input streams 
    sockets_list = [sys.stdin, server] 

    # """ There are two possible input situations. Either the 
    # user wants to give  manual input to send to other people, 
    # or the server is sending a message  to be printed on the 
    # screen. Select returns from sockets_list, the stream that 
    # is reader for input. So for example, if the server wants 
    # to send a message, then the if condition will hold true 
    # below.If the user wants to send a message, the else 
    # condition will evaluate as true"""
    print("wwwwwwwwwwwwwwwwwwwwwww")
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
    print("eeeeeeeeeeeeeeeeeeeeeeeeeeeee")
    for socks in read_sockets: 
        if socks == server: 
            print("llego")
            message = socks.recv(2048).decode() 
            print (message) 
        else: 
            message = sys.stdin.readline() 
            server.send(message) 
            sys.stdout.write("<You>") 
            sys.stdout.write(message) 
            sys.stdout.flush() 

print("holi")
server.close() 