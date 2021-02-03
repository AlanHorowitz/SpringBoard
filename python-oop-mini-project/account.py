class AccountTransactionAbortedException(Exception):
    pass

class AccountTransactionFailedException(Exception):
    pass

class Account():

    ACCOUNT_TYPES = ['CHECKING', 'SAVINGS']
    SAVINGS_ID_PREFIX = "SAV"
    CHECKING_ID_PREFIX = "CHK"
    STANDARD_OPTIONS =[]
    QUIT = 'quit'

    @staticmethod
    def create_new_account(customer, id):
        '''
        Factory method for creating a variety of Accounts.
        '''
        print("Which type of account would you like to create?")
        print("")
        print("[1] Checking")
        print("[2] Savings")
        print("[3] Quit")
        print("")

        print("Please Enter from menu. Use [3] to quit: ", end='')
        s = ""

        while True:
            print("Please Enter from menu. Use [3] to quit: ", end='')
            s = input().strip()
            if s == "1":
                return CheckingAccount(customer, id)
            elif s == "2":
                return SavingsAccount(customer, id)
            elif s == "3":
                raise AccountTransactionAbortedException
         
    def __init__(self, customer, id):
        self.customer = customer
        self.id = id
    def get_options(self):
        self.options.extend(Account.STANDARD_OPTIONS)
        d = {}
        for i, opt in enumerate(self.options,start=1):
            print(option[0])
            d[str(i)] = option[1]
        
        while True:
            print(f"Please Enter from menu. Use [{i}] to quit: ", end='')
            s = input().strip()
            if s in d:
                if d[s] == Account.QUIT:
                    raise AccountTransactionAbortedException
                else:
                    getattr(self, d[s])()  # call the function

        
                

    def deposit(self): pass
    def transfer(self): pass

class SavingsAccount(Account):
    
    def __init__(self, customer, id):
        super.__init__(self, customer, id)
        self.account_id = Account.SAVINGS_ID_PREFIX + id   
        
    def withdraw(self): pass

    
class CheckingAccount(Account):

    def __init__(self, customer, id):
        super.__init__(self, customer, id)
        self.account_id = Account.CHECKING_ID_PREFIX + id 

    def order_checks(self):
        pass

    def write_check(self):
        pass 