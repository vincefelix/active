#!/usr/bin/env python3

import argparse
import socket
import sys
import concurrent.futures

def get_service_name(port, protocol):
    """Retourne le nom du service associé à un port, sinon 'Unknown'."""
    try:
        return socket.getservbyport(port, protocol)
    except OSError:
        return "Unknown"

def scan_port(host, port, udp=False):
    """
    Scanne un port en TCP ou UDP.
    Retourne un tuple (port, status, service) si le scan a pu être effectué,
    sinon None en cas d'erreur.
    """
    sock = None  # Initialisation pour le bloc finally
    try:
        port = int(port)
        if port < 1 or port > 65535:
            print(f"❌ Erreur : Le port {port} est invalide. (Doit être entre 1 et 65535)")
            return None

        service = get_service_name(port, "udp" if udp else "tcp")

        if udp:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            sock.sendto(b"", (host, port))
            try:
                sock.recvfrom(1024)  # Essaye de recevoir une réponse
                status = "open"
            except socket.timeout:
                status = "closed"
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            status = "open" if result == 0 else "closed"

        return (port, status, service)

    except ValueError:
        print(f"❌ Erreur : '{port}' n'est pas un numéro de port valide.")
    except socket.gaierror:
        print(f"❌ Erreur : Hôte '{host}' introuvable.")
    except socket.error as e:
        print(f"❌ Erreur réseau sur le port {port}: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
    finally:
        if sock:
            sock.close()
    return None

def parse_ports(port_arg):
    """
    Parse une plage de ports sous forme '80' ou '80-83'.
    Retourne une liste ou un range de ports.
    """
    try:
        if "-" in port_arg:
            start, end = map(int, port_arg.split("-"))
            if start > end:
                print("❌ Erreur : La plage de ports est invalide.")
                sys.exit(1)
            return range(start, end + 1)
        return [int(port_arg)]
    except ValueError:
        print("❌ Erreur : Format de port invalide. Utilisez un nombre ou une plage (ex: 80 ou 80-83).")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Simple Port Scanner",
        usage="tinyscanner [OPTIONS] [HOST] [PORT]"
    )
    parser.add_argument("host", type=str, help="L'adresse IP ou le nom d'hôte à scanner")
    parser.add_argument("-p", "--port", required=True,
                        help="Port ou plage de ports à scanner (ex: 80 ou 80-83)")
    parser.add_argument("-u", "--udp", action="store_true", help="Scanner en mode UDP")
    parser.add_argument("-t", "--tcp", action="store_true", help="Scanner en mode TCP")
    parser.add_argument("-n", "--threads", nargs='?', const=100, type=int,
                        help=("Nombre de threads à utiliser pour le scan (entre 2 et 100). "
                              "Si non spécifié, le scan se fait séquentiellement. "
                              "Si utilisé sans valeur, la valeur par défaut sera 100."))
    args = parser.parse_args()

    if not (args.udp or args.tcp):
        print("❌ Erreur : Veuillez spécifier -t pour TCP ou -u pour UDP")
        sys.exit(1)

    ports = parse_ports(args.port)
    results = []

    if args.threads is not None:
        # Vérification du nombre de threads
        if args.threads < 2 or args.threads > 100:
            print("❌ Erreur : Le nombre de threads doit être compris entre 2 et 100.")
            sys.exit(1)
        thread_count = args.threads
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)
        futures = [executor.submit(scan_port, args.host, port, udp=args.udp) for port in ports]

        try:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None:
                    port, status, service = result
                    print(f"Port {port} is {status} ({service})")
                    results.append(result)
        except KeyboardInterrupt:
            print("\nSignal received. Aborting scan...")
            for future in futures:
                future.cancel()
            executor.shutdown(wait=False)
            sys.exit(1)
        finally:
            executor.shutdown(wait=False)
    else:
        # Scan séquentiel
        try:
            for port in ports:
                result = scan_port(args.host, port, udp=args.udp)
                if result is not None:
                    port, status, service = result
                    print(f"Port {port} is {status} ({service})")
                    results.append(result)
        except KeyboardInterrupt:
            print("\nSignal received. Aborting scan...")
            sys.exit(1)

    # Résumé final : affichage des ports ouverts avec leur service
    open_ports = [(port, service) for port, status, service in results if status == "open"]
    if open_ports:
        summary = "\n".join([f"{port} ({service})" for port, service in open_ports])
        print(f"\nThe open ports are: \n{summary}")
    else:
        print("\nNo open ports found.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan aborted by user.")
        sys.exit(1)
