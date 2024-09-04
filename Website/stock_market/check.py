import socket

class Stock:
    def __init__(self):
        self.outstanding_shares = 4.7*10**9
        self.constant = 2.35*10**11
        self.price = self.constant/self.outstanding_shares
        self.transactions = []

    def update_price(self, outstanding_shares):
        self.price = self.constant/outstanding_shares
        self.send_price_to_stock()

    def sell(self, no_of_shares):
        self.outstanding_shares += no_of_shares
        self.transactions.append({
                    'quantity': no_of_shares, 
                    'price': self.price
                })
        return self.update_price(self.outstanding_shares)

    def buy(self, no_of_shares):
        self.outstanding_shares -= no_of_shares
        self.transactions.append({
                    'quantity': no_of_shares, 
                    'price': self.price
                })
        return self.update_price(self.outstanding_shares)

    def send_price_to_stock(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(('localhost', 65432))  # Connect to stock.py
                sock.sendall(str(self.price).encode('utf-8'))
                print(f"Sent updated price: {self.price} to stock.py")
        except ConnectionRefusedError:
            print("Failed to connect to stock.py. Make sure it is running.")
