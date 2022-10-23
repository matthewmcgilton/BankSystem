import queue
from transaction import Transaction
from account import Account

class Bank():
    def __init__(self):
        #Creates a queue for holding txs and a binary tree for storing accounts
        self.tx_queue = queue.Queue()
        self.accounts = AccountBinarySearchTree() 

    #Function which takes the each line in the file and puts them into a queue as strings
    def read_transactions(self, file):
        try:
            transactions = open(file, "r")
        except:
            print("BankTransIn.txt file not found in directory")
            exit()
        
        #Scanning each line and adding to queue
        for line in transactions:
            line = line.rstrip() #rstrip to remove /n from each line
            self.tx_queue.put(line)

        transactions.close()

    #Function which takes each string from the queue, makes a tx object and then performs the task of the object
    def process_transactions(self):
        #Loop to iterate through the queue
        for i in range(0, self.tx_queue.qsize()):
            #Getting current tx object
            current_tx = Transaction(self.tx_queue.get()) #Split done so elements of the tx string are separated

            #Statement to make sure only correctly formatted transactions are run
            if current_tx.correct == True:
                #Creating current account object
                current_account = self.accounts.get(current_tx.id)

                #Opening a new account
                if(current_tx.command == "O" and current_tx.correct == True):
                    #Making sure account does not exist already
                    if(current_account == None):
                        new_account = Account(current_tx) #Creating new account using info from the tx object
                        self.accounts.put(new_account.id, new_account) #Adding ID and account object to binary tree
                    else:
                        print("ERROR: Account {} is already open. Transaction refused.".format(current_tx.id))
                
                #Otherwise do something to an existing account
                elif(current_account != None):  
                    #Deposit
                    if(current_tx.command == "D"):
                        if not current_account.fund.deposit(current_tx.fund, current_tx.amount):
                            current_account.add_history(current_tx.fund, current_tx.tx + " (Failed)")
                        else:
                            current_account.add_history(current_tx.fund, current_tx.tx)
                    
                    #Withdrawal
                    elif(current_tx.command == "W"):
                        #If withdraw fails then there wasn't enough money, otherwise withdrawal is done correctly
                        if not current_account.fund.withdraw(current_tx.fund, current_tx.amount, False):
                            current_account.add_history(current_tx.fund, current_tx.tx + " (Failed)")
                            
                            #Items for the error statement
                            amt = current_tx.amount
                            first = current_account.first
                            last = current_account.last
                            fundname = current_account.fund.__repr__(current_tx.fund)
                            
                            print("ERROR: Not enough funds to withdraw {} from {} {} {}".format(amt, first, last, fundname))

                    #Transfer
                    elif(current_tx.command == "T"):
                        #Get account receiving funds
                        other_account = self.accounts.get(current_tx.otherid)
                        
                        #If the other account exists, otherwise account not found error.
                        if(other_account != None):
                            #Remove amount from current account and add to other
                            #Statement to make sure withdrawal was properly completed before deposit is allowed to happen
                            if(current_account.fund.withdraw(current_tx.fund, current_tx.amount, True)):
                                other_account.fund.deposit(current_tx.otherfund, current_tx.amount)
                                current_account.add_history(current_tx.fund, current_tx.tx)
                                other_account.add_history(current_tx.otherfund, current_tx.tx)
                        else:
                            current_account.add_history(current_tx.fund, current_tx.tx + " (Failed)")
                            print("ERROR: Account {} not found. Transferal refused.".format(current_tx.otherid))
                    
                    #Display history
                    elif(current_tx.command == "H"):
                        try:
                            current_account.display_history(current_tx.fund)
                        except AttributeError:
                            current_account.display_history()

                #If this case is reached then the account attempted to be modified doesn't exist
                else:
                    print("ERROR: Account with that ID doesn't exist. Transaction refused.")

    #Returns all of the accounts in the bank and their balances.
    def __str__(self):
        value = "\nProcessing Done. Final Balances"

        #Loops through all of the accounts in each tree in order
        for account in self.accounts.in_order_traversal(AccountNode):
            value += "\n{} {} Account ID: {}\n".format(account.first, account.last, account.id)
            
            #Loop to add the value for each fund type within the account
            for i in range(0, 10):
                value += "    " + account.fund.__str__(i) + "\n"
        
        return value

#Account node
class AccountNode:
    def __init__(self, key, value = None):
        self.key = key
        self.value = value

        #Start with node having no children
        self.left_child = None
        self.right_child = None

    def is_leaf(self):
        return self.left_child == None and self.right_child == None

    def __str__(self):
        return str(self.key) + " " + str(self.value)

#Account BST
class AccountBinarySearchTree:
    def __init__(self):
        self._count = 0 #number of nodes
        self._root = None #pointer

    def size(self):
        return self._count

    def get(self, key):
        current_node = self._root
        while current_node != None:
            if current_node.key == key:
                return current_node.value
            elif current_node.key > key:
                current_node = current_node.left_child
            else:
                current_node = current_node.right_child
        return None
    
    def put(self, key, value):
        #if its an empty tree
        if self._count == 0:
            self._root = AccountNode(key, value)
            self._count += 1
            return
        current_node = self._root
        while True:
            if current_node.key == key:
                current_node.value = value
                return
            elif current_node.key > key:
                if current_node.left_child == None:
                    new_node = AccountNode(key, value)
                    current_node.left_child = new_node
                    break
                else:
                    current_node = current_node.left_child
            else:
                if current_node.right_child == None:
                    new_node = AccountNode(key, value)
                    current_node.right_child = new_node
                    break
                else:
                    current_node = current_node.right_child
        self._count += 1

    def remove(self, key):
        if self._root == None:
            return False
        
        if self._root.key == key:
            self._count -= 1
            if self._root.left_child == None:
                self._root = self._root.right_child
            elif self._root.right_child == None:
                self._root = self._root.left_child
            else:
                replace_node = self.get_remove_right_small(self._root)
                self._root.key = replace_node.key
                self._root.value = replace_node.value
        else:
            current_node = self._root
            while current_node != None:
                if current_node.left_child and current_node.left_child == key:
                    found_node = current_node.left_child
                    if found_node.is_leaf():
                        current_node.left_child = None
                    elif found_node.right_child == None:
                        current_node.left_child = found_node.left_child
                    elif found_node.left_child == None:
                        current_node.left_child = found_node.right_child
                    else:
                        replace_node = self.get_remove_right_small(found_node)
                        found_node.key = replace_node.key
                        found_node.value = replace_node.value
                        count -= 1
                        return True
                elif current_node.right_child and current_node.right_child.key == key:
                    pass
                elif current_node.key > key:
                    current_node = current_node.left_child
                else:
                    current_node = current_node.right_child

    def in_order_traversal(self, func):
        self.return_list = []
        self.in_order_traversal_r(self._root, func)
        return self.return_list
        
    def in_order_traversal_r(self, node, func):
        if node != None:
            self.in_order_traversal_r(node.left_child, func)
            func(node.key, node.value)
            self.return_list.append(node.value)
            self.in_order_traversal_r(node.right_child, func)

    def __setitem__(self, key, data):
        self.put(key, data)

    def __getitem__(self, key):
        return self.get(key)