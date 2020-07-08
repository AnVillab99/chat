# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
import os
import LLaves as keys
from _thread import *
from Crypto.PublicKey import RSA
import random, sys, math
from Crypto.Cipher import PKCS1_OAEP
import binascii





# """The first argument AF_INET is the address domain of the 
# socket. This is used when we have an Internet Domain with 
# any two hosts The second argument is the type of socket. 
# SOCK_STREAM means that data or characters are read in 
# a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 

# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 

# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 

# """ 
# binds the server to an entered IP address and at the 
# specified port number. 
# The client must be aware of these parameters 
# """
server.bind((IP_address, Port)) 

# """ 
# listens for 100 active connections. This number can be 
# increased as per convenience. 
# """
server.listen(100) 

list_of_clients = [] 
keys.generateKeys()
def clientthread(conn, addr): 
    # sends a message to the client whose user object is conn 
    size = int(conn.recv(2048).decode())
    f = open(str(addr)+"Pkey.pem","wb")
    for i in range ((size//2048)+1):
        bytes_read = conn.recv(2048)
        if not bytes_read:    
            # nothing is received
            # file transmitting is done
            break
        f.write(bytes_read)
    mes= "Welcome to this chatroom!"
    #--------------------------------Envia al cliente la publica ------------------------------------------------------
    f =open("public.pem", "rb")
    filesize = os.path.getsize("public.pem")
    conn.send(str(filesize).encode())
    for i in range ((filesize//2048)+1):
        print("una vez")
        bytes_read = f.read(2048)
        if not bytes_read:
                break
        conn.sendall(bytes_read)


    conn.send(mes.encode()) 

    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 

                    # """prints the message and address of the 
                    # user who just sent the message on the server 
                    # terminal"""
                    print("pre"+ message)
                    print ("<" + addr[0] + "> " + decrypt(message))
                    # Calls broadcast function to send message to all 
                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, conn) 
                else: 
                    # """message may have no content if the connection 
                    # is broken, in this case we remove the connection"""
                    remove(conn) 
            except: 
                continue
# """Using the below function, we broadcast the message to all 
# clients who's object is not the same as the one sending 
# the message """
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients[0]!=connection: 
            try: 
                clients[0].send(encrypt(message,clients[1]+"Pkey.pem")) 
            except: 
                clients.close() 
                # if the link is broken, we remove the client 
                remove(clients) 
# """The following function simply removes the object 
# from the list that was created at the beginning of  
# the program"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
while True: 
    # """"Accepts a connection request and stores two parameters,  
    # conn which is a socket object for that user, and addr  
    # which contains the IP address of the client that just  
    # connected"""
    print("#")
    conn, addr = server.accept() 
    print("°")
    # """Maintains a list of clients for ease of broadcasting 
    # a message to all available people in the chatroom"""
    list_of_clients.append([conn,addr]) 
    # prints the address of the user that just connected 
    print (addr[0] + " connected")
    # creates and individual thread for every user  
    # that connects 
    start_new_thread(clientthread,(conn,addr))    



 
def encrypt(message):
    f = open("public.pem", "r")
    public = RSA.import_key(f.read())
    # public (n,e)
    
    cipher = PKCS1_OAEP.new(key=public)
    cipher_text = cipher.encrypt(bytes(message, encoding="utf-8"))
    print(cipher_text)
    
    return cipher_text


def encrypt(message,file):
    f = open(file, "r")
    public = RSA.import_key(f.read())
    # public (n,e)
    
    cipher = PKCS1_OAEP.new(key=public)
    cipher_text = cipher.encrypt(bytes(message, encoding="utf-8"))
    print(cipher_text)
    
    return cipher_text

def decrypt(cipher_text):
    # private (n,d)
    f = open("private.pem", "r")
    private = RSA.import_key(f.read())
    decrypt = PKCS1_OAEP.new(key=private)
    text = decrypt.decrypt(cipher_text)
    
    return text
conn.close() 
server.close() 