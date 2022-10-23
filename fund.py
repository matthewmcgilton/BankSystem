class Fund:
    def __init__(self, parent):
        self.parent = parent
        self.funds = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0
        }
    
    def deposit(self, fund, amount):
        if(amount >= 0):
            self.funds[fund] += amount
            return True
        else:
            print("ERROR: Cannot deposit negative amounts. Transaction refused.")
    
    def withdraw(self, fund, amount, transfer):
        #If amount being withdrawn is negative, send error and fail the tx
        if(amount < 0):
            ("ERROR: Cannot withdraw negative amounts. Transaction refused.")
            return False
        
        #If fund has more than amount being withdrawn
        elif(self.funds[fund] >= amount):
            self.funds[fund] -= amount
            if(transfer == False):
                self.parent.add_history(fund, "W {}{} {}".format(self.parent.id, fund, amount))
            return True

        #If amount attempted to be withdrawn is larger than what's in the fund
        elif(self.funds[fund] < amount):
            #Difference between amount withdrawn and amount available
            difference = amount - self.funds[fund]
            #If money market, check if prime money market can cover the difference
            if(fund == 0):
                if(self.funds[1] >= difference):
                    #Only adds history if it's a withdraw and not a transfer
                    if(transfer == False):
                        self.parent.add_history(1, "W {}1 {}".format(self.parent.id, difference))
                        self.parent.add_history(0, "W {}0 {}".format(self.parent.id, self.funds[0]))
                    
                    self.funds[1] -= difference
                    self.funds[0] = 0
                    return True
            #If prime money market, check if prime money market can cover the difference
            elif(fund == 1):
                if(self.funds[0] >= difference):
                    if(transfer == False):
                        self.parent.add_history(0, "W {}0 {}".format(self.parent.id, difference))
                        self.parent.add_history(1, "W {}1 {}".format(self.parent.id, self.funds[1]))
                    
                    self.funds[0] -= difference
                    self.funds[1] = 0
                    return True
            #If long bond, check if short bond can cover the difference
            elif(fund == 2):
                if(self.funds[3] >= difference):
                    if(transfer == False):
                        self.parent.add_history(3, "W {}3 {}".format(self.parent.id, difference))
                        self.parent.add_history(2, "W {}2 {}".format(self.parent.id, self.funds[2]))
                    
                    self.funds[3] -= difference
                    self.funds[2] = 0
                    return True
            #If short bond, check if long bond can cover the difference
            elif(fund == 3):
                if(self.funds[2] >= difference):
                    if(transfer == False):
                        self.parent.add_history(2, "W {}2 {}".format(self.parent.id, difference))
                        self.parent.add_history(3, "W {}3 {}".format(self.parent.id, self.funds[3]))
                    
                    self.funds[2] -= difference
                    self.funds[3] = 0
                    return True
            #If fund is not any of these, return False as nothing can be withdrawn
            else:
                return False

    #Used to return the fund name and the value associated with the fund
    def __str__(self, fund):
        value = ""
        if(fund == 0):
            value = "Money Market: ${}".format(self.funds[0])
        elif(fund == 1):
            value = "Prime Money Market: ${}".format(self.funds[1])
        elif(fund == 2):
            value = "Long-Term Bond: ${}".format(self.funds[2])
        elif(fund == 3):
            value = "Short-Term Bond: ${}".format(self.funds[3])
        elif(fund == 4):
            value = "500 Index Fund: ${}".format(self.funds[4])
        elif(fund == 5):
            value = "Capital Value Fund: ${}".format(self.funds[5])
        elif(fund == 6):
            value = "Growth Equity Fund: ${}".format(self.funds[6])
        elif(fund == 7):
            value = "Growth Index Fund: ${}".format(self.funds[7])
        elif(fund == 8):
            value = "Value Fund: ${}".format(self.funds[8])
        elif(fund == 9):
            value = "Value Stock Index: ${}".format(self.funds[9])
        return value
    
    #Used to return the fund name only
    def __repr__(self, fund):
        value = ""
        if(fund == 0):
            value = "Money Market"
        elif(fund == 1):
            value = "Prime Money Market"
        elif(fund == 2):
            value = "Long-Term Bond"
        elif(fund == 3):
            value = "Short-Term Bond"
        elif(fund == 4):
            value = "500 Index Fund"
        elif(fund == 5):
            value = "Capital Value Fund"
        elif(fund == 6):
            value = "Growth Equity Fund"
        elif(fund == 7):
            value = "Growth Index Fund"
        elif(fund == 8):
            value = "Value Fund"
        elif(fund == 9):
            value = "Value Stock Index"
        return value