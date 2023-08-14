import socket
import threading

# Settings del server
address = "127.0.0.1"
port = 50777

# Array dei client
clients = {}

# ID client
client_id = 0

# Gestione client
def handle_client(client_socket, client_address):
    print(f"\nClient connesso! IP: {client_address}")

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

    client_socket.close()

# Selezione del client per l'invio del messaggio
def select_client(client_socket):
    while True:
        client_id_input = input("Inserisci l'ID del client a cui vuoi inviare il messaggio: ")
        try:
            client_id = int(client_id_input)
            if client_id in clients:
                message = input("Inserisci il messaggio da inviare: ")
                send_message_to_client(client_id, message)
                break  # Esci dal ciclo se tutto è andato bene
            else:
                print("ID del client non valido.")
        except ValueError:
            print("ID del client non valido.")

# Invio un messaggio al client_id selezionato
def send_message_to_client(client_id, message):
    if client_id in clients:
        client_socket = clients[client_id]
        if client_socket.fileno() != -1:
            client_socket.send(f"{message}".encode())
            print(f"Server invia messaggio al Client {client_id}: {message}")
        else:
            print(f"Client {client_id} non trovato o connessione chiusa.")
    else:
        print(f"Client {client_id} non trovato.")

# Menu principale
def main_menu():
    while True:
        print("\nMENU:")
        print("1. Invia messaggio a un client")
        print("2. Visualizza lista client connessi")
        print("3. Esci")

        choice = input("Seleziona un'opzione: ")

        if choice == '1':
            select_client(client_socket)
        elif choice == '2':
            print_clients()
        elif choice == '3':
            break
        else:
            print("Opzione non valida. Riprova.")

# Funzione per visualizzare la lista dei client connessi
def print_clients():
    print("\nLista client connessi:")
    for client_id in clients:
        print(f"Client ID: {client_id}")

# Creo oggetto socket e lo metto in ascolto
server_socket = socket.socket()
server_socket.bind((address, port))
server_socket.listen()
print(f"Il server è in ascolto sulla porta {port}...")

main_thread = threading.Thread(target=main_menu)
main_thread.start()

# Accetto la connessione in entrata e creo un nuovo Thread per ognuna
while True:
    # Accetto la connessione
    client_socket, client_address = server_socket.accept()

    client_id += 1
    clients[client_id] = client_socket

    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()



