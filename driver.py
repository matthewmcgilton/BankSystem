from bank import Bank

matthews_bank = Bank()
matthews_bank.read_transactions("BankTransIn.txt")
matthews_bank.process_transactions()
print(matthews_bank)