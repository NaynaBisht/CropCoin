import socket
import threading
import time
from check import Stock

def handle_client_connection(client_socket):
    global current_price
    while True:
        # Send the current price to the client
        client_socket.sendall(current_price.encode('utf-8'))
        time.sleep(1)

def update_price(new_price):
    global current_price
    current_price = str(new_price)
    print(f"Price updated to: {current_price}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        client_handler = threading.Thread(
            target=handle_client_connection, args=(client_socket,)
        )
        client_handler.start()

if __name__ == "__main__":
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    s = Stock()

    # Simulate user updating the price
    while True:
        update_price(s.update_price(4.7*10**9))
        time.sleep(1)
