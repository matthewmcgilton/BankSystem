class Transaction:
    def __init__(self, tx):
        #Values in every transaction
        self.tx = tx #String
        self.split_tx = tx.split() #List of elements in string
        self.command = tx[0] #Command which is always the first element of the string
        self.correct = True

        #Open a new account: O Bowden Charles 6537
        if(self.command == "O"):
            self.last = self.split_tx[1]
            self.first = self.split_tx[2]
            
            #Makes sure ID is proper length
            if(len(self.split_tx[3]) == 4):
                self.id = int(self.split_tx[3])
            else:
                self.correct = False
                print("ERROR: Account IDs must be 4 numbers long. Account creation refused.")

        #Deposit/withdraw within one account: #D/W 12341 100
        elif(self.command == "D" or self.command == "W"):
            self.amount = int(self.split_tx[2])
            
            #Makes sure ID+fund is proper length of 5 characters
            if(len(self.split_tx[1]) == 5):
                #Makes sure ID is from 0 to 9:
                self.id = int(self.split_tx[1][0:4])
                self.fund = int(self.split_tx[1][4])
            else:
                self.correct = False
                print("ERROR: Account IDs must be 4 numbers long and fund must be from 0 to 9. Transaction refused.")

        #Transfer from account to other account: #T 12340 1000 12341
        elif(self.command == "T"):
            self.amount = int(self.split_tx[2])
            #Makes sure both accounts give the ID and fund (5 characters)
            if (len(self.split_tx[1]) == 5 and len(self.split_tx[3]) == 5):
                self.id = int(self.split_tx[1][0:4])
                self.fund = int(self.split_tx[1][4])
                self.otherid = int(self.split_tx[3][0:4])
                self.otherfund = int(self.split_tx[3][4])
            else:
                self.correct = False
                print("ERROR: Account IDs must be 4 numbers long and fund must be from 0 to 9. Transferal refused.")


        #Show history of an account: #H 1234, #H 12340
        elif(self.command == "H"):
            #If only ID given, should be 4 characters
            if(len(self.split_tx[1]) == 4):
                self.id = int(self.split_tx[1])
            #If ID and fund given, should be 5 characters
            elif(len(self.split_tx[1]) == 5):
                self.id = int(self.split_tx[1][0:4])
                self.fund = int(self.split_tx[1][4])
            else:
                self.correct = False
                print("ERROR: Account IDs must be 4 numbers long and fund must be from 0 to 9. History request refused.")