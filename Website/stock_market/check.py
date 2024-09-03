class Stock:
    def __init__(self):
        self.outstanding_shares = 4.7*10**9
        self.constant = 2.35*10**11
        self.transactions = []

    def update_price(self, outstanding_shares):
        current_price = self.constant/outstanding_shares
        return str(current_price)

    def sell(self, current_price, no_of_shares):
        self.outstanding_shares += no_of_shares
        self.transactions.append({
                    'quantity': no_of_shares, 
                    'price': current_price
                })
        return self.update_price(self.outstanding_shares)

    def buy(self, current_price, no_of_shares):
        self.outstanding_shares -= no_of_shares
        self.transactions.append({
                    'quantity': no_of_shares, 
                    'price': current_price
                })
        return self.update_price(self.outstanding_shares)

