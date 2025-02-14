import socket
import sys

def start_udp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f"Serveur UDP lancé sur {host}:{port}")

    try:
        while True:
            message, client_address = server_socket.recvfrom(1024)
            print(f"Reçu de {client_address}: {message.decode()}")
            response = "Réponse du serveur UDP"
            server_socket.sendto(response.encode(), client_address)

    except KeyboardInterrupt:
        print("\nServeur interrompu par l'utilisateur.")
    finally:
        server_socket.close()
        print("Socket UDP fermé. Serveur arrêté.")

if __name__ == "__main__":
    start_udp_server("127.0.0.1", 1100)
