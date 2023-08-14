import socket
import threading

address = "127.0.0.1"
port = 50777

def send_commands(client_socket):
    while True:
        command = input("Inserisci un comando da mandare al server: ")
        client_socket.send(command.encode())
        
        if command == 'exit':
            break

def receive_responses(client_socket):
    while True:
        response = client_socket.recv(1024)
        if not response:
            break
        print("\nRisposta dal server:", response.decode())

try:
    client_socket = socket.socket()
    client_socket.connect((address, port))
    print(f"Client connesso al server {address}")

    send_thread = threading.Thread(target=send_commands, args=(client_socket,))
    receive_thread = threading.Thread(target=receive_responses, args=(client_socket,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

except Exception as e:
    print("Errore:", e)

finally:
    client_socket.close()
    print("Connessione chiusa.")
