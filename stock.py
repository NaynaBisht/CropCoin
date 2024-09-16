import asyncio
import websockets
import socket
import threading

price = 50  # Initial price
price_lock = threading.Lock()

# This function will handle broadcasting the price via WebSockets
async def broadcast_price(websocket):
    global price
    try:
        while True:
            with price_lock:
                current_price = price
            await websocket.send(str(current_price))
            await asyncio.sleep(1)  # Broadcast every second
    except websockets.ConnectionClosed as e:
        print(f"WebSocket connection closed with code {e.code}")

# This function will handle updating the price received from check.py
def update_price():
    global price
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen(1)
    print("Waiting for connection to update price...")
    
    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if data:
                with price_lock:
                    price = float(data.decode('utf-8'))
                    print(f"Updated price: {price}")

# This function starts the WebSocket server and listens for connections to broadcast the price
async def main():
    start_server = websockets.serve(broadcast_price, "localhost", 8765)
    await start_server
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    # Run the update_price function in a separate thread to listen for price updates
    threading.Thread(target=update_price, daemon=True).start()
    
    # Start the WebSocket server
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Process interrupted.")

