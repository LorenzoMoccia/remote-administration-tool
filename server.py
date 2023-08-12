import socket
import threading

#Settings del server
address = "127.0.0.1"
port = 50777

#Gestione client
def handle_client(client_socket, client_address):
    print(f"Client connesso! IP: {client_address}")


#Ricevo ed invio dati al client
    while True:
        try:
            data = client_socket.recv(2048)

            if not data:
                break

            command = data.decode()
            message = "Comando ricevuto!"
            client_socket.send(message.encode())

            print(f"{client_address}: {command} ")

            if command == 'exit':
                print(f"CLIENT {client_address} si è disconnesso!")

        except BrokenPipeError:
            print("Connessione chiusa dal client.")
            break

    #Chiudo la connessione del client
    client_socket.close()

#Creo oggetto socket e lo metto in ascolto
server_socket = socket.socket()
server_socket.bind((address, port))
server_socket.listen()
print(f"Il server è in ascolto sulla porta {port}...")


#Accetto la connessione in entrata e creo un nuovo Thread per ognuna
while True:
    client_socket, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
    


