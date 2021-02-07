class TransactionFailedException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

class Account():

    def __init__(self, customer_id=None):  
        self._balance = 0
        self._customer_id = customer_id
        self._id = None        

    open_metadata = {'open': ('No Display',[('opening_balance', 'Please enter a starting balance', 'non_negative_float')])}
    def open(self,opening_balance=100):
        self._balance = opening_balance
      
    deposit_metadata = {'deposit' : ('Deposit to account', [('deposit_amount', 'Please enter amount to deposit: ', 'non_negative_float')])}
    def deposit(self, deposit_amount=0):
        self._balance += deposit_amount

    def get_open_metadata(self):
        return Account.open_metadata

    def get_transaction_metadata(self):
        return Account.deposit_metadata

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

    withdraw_metadata = {'withdraw' : ('Withdraw from account', [('withdrawal_amount', 'Please enter amount to withdraw','non_negative_float')])}
    def withdraw(self,withdrawal_amount=0): 
        if withdrawal_amount > self._balance:
            raise TransactionFailedException(f"Withdrawal amount {withdrawal_amount} exceeded balance {self._balance}") 
        self._balance -= withdrawal_amount

    def get_transaction_metadata(self): 
        d = super().get_transaction_metadata()
        d.update(SavingsAccount.withdraw_metadata)
        return d
    
class CheckingAccount(Account):

    CHECKING_ID_PREFIX = "CHK"
    next_checking_account_id = 1

    def __init__(self, customer_id=None): 
        super().__init__(customer_id)
        self._id = CheckingAccount.CHECKING_ID_PREFIX + str(CheckingAccount.next_checking_account_id)
        CheckingAccount.next_checking_account_id += 1

    open_metadata = {'open': ('No Display',[('opening_balance', 'Please enter a starting balance: ', 'non_negative_float'),
                                            ('number_starter_checks','Please enter your initial number of checks (default is 10): ', 'non_negative_int' )])}

    def open(self,opening_balance=100, number_starter_checks=10): 
        super().open(opening_balance)
        self._remaining_checks = number_starter_checks

    order_checks_metadata = {'order_checks' : ('Order replacement checks ($5 per 50 checks will be deducted from balance) ',
     [('number_of_checks', 'Please enter number of new checks: ', 'non_negative_int')])}
    def order_checks(self,number_of_checks=0): 
        cost_of_checks = number_of_checks * .1
        if self._balance >= cost_of_checks:
            self._balance -= cost_of_checks
            self._remaining_checks += number_of_checks
        else:
            raise TransactionFailedException(f"Insufficient balance ({self._balance}) to purchase checks ") 

    write_check_metadata = {'write_check' : ('Write a check',
    [('check_amount', 'Please enter the check amount: ', 'non_negative_float')])}
    def write_check(self, check_amount=0):  
        if check_amount > self._balance:
            raise TransactionFailedException(f"Insufficient balance ({self._balance}) to write check. ") 
        elif self._remaining_checks < 1:
            raise TransactionFailedException("Out of checks. Please purchase checks. ") 
        else:
            self._balance -= check_amount
            self._remaining_checks -= 1 

    def get_open_metadata(self):
        d = super().get_open_metadata()
        d.update(CheckingAccount.open_metadata)
        return d

    def get_transaction_metadata(self):  
        d = super().get_transaction_metadata()
        d.update(CheckingAccount.write_check_metadata)
        d.update(CheckingAccount.order_checks_metadata)
        return d
                 

    