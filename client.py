import socket
import sys

address = "127.0.0.1"
port = 50777

#Creo l'oggetto socket
client_socket = socket.socket()


try:
    client_socket.connect((address, port))
    print(f"Client connesso al server {address}")


    while True:
        command = input("Inserisci un comando da mandare al server: ")
        client_socket.send(command.encode())

        if command == 'exit':
            break

        response = client_socket.recv(1024)
        print("Risposta dal server:", response.decode())

except Exception as e:
    print("Errore:", e)

finally:
    client_socket.close()
    print("Connessione chiusa.")