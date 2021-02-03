class Account():

    def __init__(self): pass
    open_metadata = {'open': ('No Display',[('opening_balance', 'Please enter a starting balance')])}
    def open(self,opening_balance=100):  
        self.balance = opening_balance
    deposit_metadata = {'deposit' : ('Deposit to account', [('a1', 'Please enter a1'),('b1', 'Please enter b1')])}
    def deposit(self,a1,b1): pass
    transfer_metadata = {'transfer': ('Transfer between accounts',[('c1', 'Please enter c1')])}
    def transfer(self,c1): pass
    def get_open_metadata(self):
        return self.open_metadata
    def get_transaction_metadata(self):
        d = {}
        d.update(self.deposit_metadata)
        d.update(self.transfer_metadata)
        return d
   
class SavingsAccount(Account):
    
    def __init__(self): pass
    open_metadata = {'open': ('No Display',[('opening_balance', 'Please enter a starting balance')])}
    def open(self,opening_balance=100):
        self.balance = opening_balance
    def get_transaction_metadata(self): pass
    def withdraw(self,d2): pass

    
class CheckingAccount(Account):

    def __init__(self): pass

    open_metadata = {'open': ('No Display',[('opening_balance', 'Please enter a starting balance'),
                                            ('number_starter_checks','Please enter your initial number of checks (default is 10)' )])}
    def open(self,opening_balance=100, number_starter_checks=10): 
        super().open(opening_balance)
        self.remaining_checks = number_starter_checks
        
    def get_transaction_metadata(self):  
        d = super().get_transaction_metadata()
        d.update(self.deposit_metadata())
        return d
                 
    def deposit_metadata(self):
        d = {'deposit' : ('Deposit to account',[('a3', 'Please enter a3'),('b3', 'Please enter b3'),
                                               ( 'c3', 'Please enter c3')])}
        return d
    def deposit(self,a3,b3,c3): pass
    def order_checks(self,e3): pass
    def write_check(self,f3):  pass