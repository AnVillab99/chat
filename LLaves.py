from Crypto.PublicKey import RSA
import random, sys, math
from Crypto.Cipher import PKCS1_OAEP
import binascii

keysize = 1024

def generateKeys():
    print("Generando números primos . . . \n")
    keyA = RSA.generate(2 * keysize)
    p,q = keyA.p , keyA.q
    print("------------------------------> Guardando llave privada")
    file = open("private.pem", "w+b")
    file.write(keyA.exportKey("PEM"))
    file.close()
    print("------------------------------> Guardando llave pública")
    file = open("public.pem", "w+b")
    file.write(keyA.publickey().exportKey("PEM"))
    file.close()
    
def encrypt(message):
    f = open("public.pem", "r")
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
    
def main():
    print("------------------------------------SPTI---------------------------------------")
    opcion = input("Inserte opcion:\n 1) Generar llaves  2) Cifrar 3) Descifrar 4) Salir:   ")
    while(opcion!="4"):
        if(opcion=="1"):
            generateKeys()
        elif(opcion=="2"):
            message = input("Digite el mensaje:     \n")
            output = encrypt(message)
            file = input("Digite el archivo:     \n")            
            file = open(file, "w+b")
            file.write(output)
            file.close()        
        elif(opcion=="3"):
            file = input("Digite el archivo:     \n")
            text = open(file, "r+b")
            message = text.read()
            print(message)
            text.close()
            output = decrypt(message)
            file = open(file+".out", "w+b")
            file.close()
            print("---------------------  > Result:  " +  output.decode("utf-8"))

        opcion = input("Inserte opcion:\n 1) Generar llaves  2) Cifrar 3) Descifrar 4) Salir:   ")
    print("------------------------------------SPTI---------------------------------------")
main()
