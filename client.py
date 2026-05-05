import socket
import threading
import sys
from colorama import Fore, Style, init

init(autoreset=True)

HOST = '127.0.0.1'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def receive():
    """Continuously listen for messages from the server and print them."""
    while True:
        try:
            message = client.recv(4096).decode("utf-8")
            if message:
                print(message, end="", flush=True)
        except:
            print(Fore.RED + "\n[!] Connection to server lost." + Style.RESET_ALL)
            client.close()
            sys.exit()

def write():
    """Read user input and send it to the server."""
    while True:
        try:
            msg = input()
            client.send(msg.encode("utf-8"))
        except:
            break

def main():
    try:
        client.connect((HOST, PORT))
        print(Fore.GREEN + Style.BRIGHT + f"[+] Connected to {HOST}:{PORT}\n" + Style.RESET_ALL)
    except:
        print(Fore.RED + "[!] Could not connect to server. Is it running?" + Style.RESET_ALL)
        sys.exit()

    # Background thread to receive messages
    threading.Thread(target=receive, daemon=True).start()

    # Main thread handles sending
    write()

if __name__ == "__main__":
    main()
