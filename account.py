from fund import Fund

class Account:
    def __init__(self, tx):
        self.first = tx.first
        self.last = tx.last
        self.id = tx.id
        self.fund = Fund(self)
        self.history = {}
    
    def add_history(self, fund, tx):
        if fund not in self.history:
            self.history[fund] = [tx]
        else:
            self.history[fund].extend([tx])
    
    def display_history(self, fund = -1):
        if fund != -1:
            print("Transaction History for {} {} {}".format(self.first, self.last, self.fund.__str__(fund)))
            for item in self.history[fund]:
                print("  " + item)
        else:
            print("Transaction History for {} {} by fund.".format(self.first, self.last))
            for i in range(0, 10):
                try:
                    if self.history[i] != None:
                        print(self.fund.__str__(i))
                        for item in self.history[i]:
                            print("  " + item)
                except:
                    pass
            