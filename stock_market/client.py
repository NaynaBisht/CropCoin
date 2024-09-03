import socket
import time

def receive_price_updates():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 65432))

    while True:
        # Receive price from server
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            print(f"Current Price: {data}")
        time.sleep(1)

if __name__ == "__main__":
    receive_price_updates()
