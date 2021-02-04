from customer import Customer, CustomerAlreadyExistsException
from account import Account, AccountTransactionAbortedException
# from bankutils import select_from_menu

def select_from_menu(header, question, options):

    print('\033c', end='')  # clear screen
    print('-' * len(header))
    print(header)
    print('-' * len(header))
    print('\n' + question + '\n')
    for i, option in enumerate(options):
        print("[" + str(i+1) + "] " + option[0])

    while True:
        print("\nPlease select an option from menu." , end='')
        s = input().strip()
        if s.isnumeric() and int(s) in range(1,len(options)+1):
            return options[int(s)-1][1]
            
class Bank():

    OPEN_NEW_ACCOUNT = "OPEN_NEW_ACCOUNT"
    RUN_TRANSACTION = "RUN_TRANSACTION"
    QUIT = "QUIT"
    YES = "YES"
    NO = "NO"

    customers = {}
    accounts = {}    

    class AccountValidationException(Exception):
        pass
    class InvalidCredentialsException(Exception):
        pass

    def persist(self):
        pass

    def welcome_user(self):

        header = "     Welcome to Simple Friendly Bank     "
        question = "What would you like to do?"
        options = (("Open a new account", Bank.OPEN_NEW_ACCOUNT),
                    ("Access an existing account", Bank.RUN_TRANSACTION),
                    ("Quit", Bank.QUIT))

        return select_from_menu(header, question, options)

    def get_new_account_type():

        header = ""
        question = "Select the desired type of account"
        options = (("Checking Account", Account.CHECKING),
                   ("Savings Account", Account.SAVINGS))

        return select_from_menu(header, question, options)
            
    def get_transaction_method(transaction_metadata):

        header = ""
        question = "Available transactions"
        options = [(transaction_metadata[meta][0], meta) for meta in transaction_metadata]  # (display_name, method)

        return select_from_menu(header, question, options)
        
    
    def open_new_account(self):

        customer = self.get_validated_customer()  
        type = self.get_new_account_type()
        if type == Account.CHECKING:
            account = CheckingAccount(customer.getId())
        if type == Account.SAVINGS:
            account = SavingsAccount(customer.getId())
        open_metadata = account.get_open_metadata()
        open_metadata_parameters = open_metadata['open'][1]
        kwargs = {parm : input(text) for parm, text in open_metadata_parameters}
        account.open(**kwargs)

        accounts[account.getID()] = account
        customer.add_account(account.getId())
        self.persist()
        input("Congratulations. You're account has been opened  Please hit return to continue")
  
    def run_transaction(self):

        account = self.get_validated_account()    
        customer = customers[account.get_custId()]
        print("Hi, " + {0} + 'Welcome Back!'.format(customers.get_customer_id()))  
        transaction_metadata = account.get_transaction_metadata()
        transaction_method  = self.get_transaction_method(transaction_metadata)  # pick desired function from menu
        transaction_parameters = transaction_metadata[transaction_method][1]
        kwargs = {parm : input(text) for parm, text in transaction_parameters}
        getattr(account, transaction_method)(**kwargs)                           # call method

        input("Congratulations. Transaction completed successfully.  Please hit return to continue")

    def run(self):

        while True:
            try:
                activity = welcome_user()
                if activity == Bank.RUN_TRANSACTION:
                    self.run_transaction()
                elif activity == Bank.OPEN_NEW_ACCOUNT:
                    self.open_new_account()
                elif activity == Bank.QUIT:
                    print("\nThank you for visiting us.  Have a great day!")
                    break
                else:
                    print("\nSystem Error")
                    break
            # handle all exceptions  here
            except(Exception):
                input("error message.  Please hit return to continue")

    def get_validated_customer(self):

        header =   "         Open a new account              "
        question = "Are you an existing customer?"
        options = (("Yes", Bank.YES),
                    ("No", Bank.NO))

        option = select_from_menu(header, question, options)            
        if option == Bank.YES:
            print("")
            customer_id = input("Please enter your customer id: ").strip()
            pin = input("Please enter your pin: ").strip()
            customer = self.customers.get(customer_id)
            if customer == None or customer.pin != pin:
                raise self.InvalidCredentialsException 
            return customer
        elif option == Bank.NO:               
            return self.get_new_customer()
        else:
            raise BankSystemError

    def get_new_customer(self):
            '''
            Interact with the user to collect necessary infomation.  Return the new customer or raise an exception if the customer already exists
            or there are validation errors.
            '''
            customer = Customer()

            print("")
            print("OK.  Let's sign you up with the following information") 

            info_metadata = customer.get_info_metadata()
            info_metadata_parameters = info_metadata['set_info'][1]
            kwargs = {parm : input(text) for parm, text in info_metadata_parameters}
            customer.set_info(**kwargs)            
                        
            if cust in self.customers.values():    # customer equality based on first_name, last_name ssn
                raise CustomerAlreadyExistsException
            else:
                self.customers[customer.getId()] = customer    # add to working dictionary    
                print("\nCongratulations, You are our new customer! Your customer id is: {n}.".format(n=cust.customer_id)) 
                print("\nPlease remember this id and your pin for future transactions.")
                input("Please hit return to continue")
                return customer

    
    def get_validated_account(self):
        
        # look for id in accounts dictionary and then check pin
        account_id =  input("\Please enter your account id ").strip()     
        pin        =  input("\nPlease enter your PIN ").strip()

        accounts.get(account_id)
        if account:            
            customer = customers[account.get_customerId()]
            if pin == customer.getPin():      
                return account

        raise(InvalidCredentialsException)

    