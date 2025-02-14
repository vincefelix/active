import socket
import sys

def start_tcp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Serveur TCP lancé sur {host}:{port}")
    
    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connexion de {client_address}")
            message = "Bienvenue sur le serveur TCP\n"
            client_socket.sendall(message.encode()) 
            client_socket.close()
    except KeyboardInterrupt:
        print("\nServeur interrompu par l'utilisateur.")
    finally:
        server_socket.close()
        print("Socket TCP fermé. Serveur arrêté.")

if __name__ == "__main__":
    start_tcp_server("127.0.0.1", 8080)
