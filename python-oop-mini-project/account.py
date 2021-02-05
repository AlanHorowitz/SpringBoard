class TransactionFailedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)
class Account():

    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"

    def __init__(self, customer_id=None):  
        self._balance = 0
        self._customer_id = customer_id
        self._id = None

    open_metadata = {'open': ('No Display',[('opening_balance', 'Please enter a starting balance')])}
    def open(self,opening_balance=100):
        if isinstance(opening_balance,str):      # comes in as string from menu
            if opening_balance.isnumeric():
                opening_balance = int(opening_balance)
            else:
                raise TransactionFailedException(f"Opening balance {opening_balance} is not numeric")   
        self._balance = opening_balance

    deposit_metadata = {'deposit' : ('Deposit to account', [('deposit_amount', 'Please enter amount to deposit: ')])}
    def deposit(self, deposit_amount=0):
        self._balance += deposit_amount

    transfer_metadata = {'transfer': ('Transfer between accounts',[('c1', 'Please enter c1')])}
    def transfer(self,c1): pass

    def get_open_metadata(self):
        return self.open_metadata

    def get_transaction_metadata(self):
        d = {}
        d.update(self.deposit_metadata)
        d.update(self.transfer_metadata)
        return d

    @property
    def id(self):
        return self._id

    @property
    def customer_id(self):
        return self._customer_id
   
class SavingsAccount(Account):

    SAVINGS_ID_PREFIX = "SAV"
    next_savings_account_id = 1
    
    def __init__(self, customer_id=None):  
        super().__init__(customer_id)
        self._id = SavingsAccount.SAVINGS_ID_PREFIX + str(SavingsAccount.next_savings_account_id)
        SavingsAccount.next_savings_account_id += 1

    withdraw_metadata = {'withdraw' : ('Withdraw from account', [('withdrawal_amount', 'Please enter amount to withdraw')])}
    def withdraw(self,withdrawal_amount=0): 
        if isinstance(withdrawal_amount,str):      # comes in as string from menu
            if withdrawal_amount.isnumeric():
                withdrawal_amount = int(withdrawal_amount)
            else:
                raise TransactionFailedException(f"Withdrawal amount {withdrawal_amount} not numeric") 

        if withdrawal_amount > self._balance:
            raise TransactionFailedException(f"Withdrawal amount {withdrawal_amount} exceeded balance {self._balance}") 
        self._balance -= withdrawal_amount

    def get_transaction_metadata(self): 
        d = super().get_transaction_metadata()
        d.update(self.withdraw_metadata)
        return d
    
class CheckingAccount(Account):

    CHECKING_ID_PREFIX = "CHK"
    next_checking_account_id = 1

    def __init__(self, customer_id=None): 
        super().__init__(customer_id)
        self._id = CheckingAccount.CHECKING_ID_PREFIX + str(CheckingAccount.next_checking_account_id)
        CheckingAccount.next_checking_account_id += 1

    open_metadata = {'open': ('No Display',[('opening_balance', 'Please enter a starting balance: '),
                                            ('number_starter_checks','Please enter your initial number of checks (default is 10): ' )])}
    def open(self,opening_balance=100, number_starter_checks=10): 
        super().open(opening_balance)
        self._remaining_checks = number_starter_checks
        
    def get_transaction_metadata(self):  
        d = super().get_transaction_metadata()
        d.update(self.deposit_metadata)
        return d
                 

    def order_checks(self,e3): pass
    def write_check(self,f3):  pass