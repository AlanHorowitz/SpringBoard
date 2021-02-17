from simplefriendlybank.customer import Customer
from simplefriendlybank.account import Account, CheckingAccount, SavingsAccount, TransactionFailedException

def select_from_menu(header, question, options):
    '''
    Interact with the terminal user via a formatted menu.
    return selected option
    '''
    print('\033c', end='')  # clear screen
    print('-' * len(header))
    print(header)
    print('-' * len(header))
    print('\n' + question + '\n')
    for i, option in enumerate(options):
        print("[" + str(i+1) + "] " + option[0])

    while True:

        print("\nPlease select an option from the menu: ", end='')
        s = input().strip()
        if s.isnumeric() and int(s) in range(1, len(options)+1):
            return options[int(s)-1][1]

def get_parameter_of_type(text, parm_type):  
    while True:
        s = input(text).strip()
        if parm_type == 'non_negative_float':
            try:
                typed_value = round(float(s),2)
                if typed_value < 0:
                    print("Value must be a non-negative float (e.g 100.00).  Please try again")
                    continue
            except ValueError:                    
                print("Value must be a non-negative float (e.g 100.00).  Please try again")
                continue
        elif parm_type == 'non_negative_int':
            try:
                typed_value = int(s)
                if typed_value < 0:
                    print("Value must be a non-negative integer. Please try again")
                    continue
            except ValueError:
                print("Value must be a non-negative integer.  Please try again")
                continue
        else:
            typed_value = s

        return typed_value

def collect_metadata_kwargs(metadata_parameters):
    return {parm: get_parameter_of_type(text, parm_type) for parm, text, parm_type in metadata_parameters}
    
class Bank():
    '''
    Controls flow using Customer and Account objects.  Talks to user dialog  Handles errors.  Performs security check
    '''

    OPEN_NEW_ACCOUNT = "OPEN_NEW_ACCOUNT"
    RUN_TRANSACTION = "RUN_TRANSACTION"
    QUIT = "QUIT"
    YES = "YES"
    NO = "NO"

    customers = {}
    accounts = {}

    class InvalidCredentialsException(Exception):
        pass
    class CustomerAlreadyExistsException(Exception):
        pass    
    class BankSystemError(Exception):
        pass 

    def menu_get_main_activity(self):
        '''
        Collect user's selection from main menu.
        ''' 
        header = "     Welcome to Simple Friendly Bank     "
        question = "What would you like to do?"
        options = (("Open a new account", Bank.OPEN_NEW_ACCOUNT),
                   ("Access an existing account", Bank.RUN_TRANSACTION),
                   ("Quit", Bank.QUIT))

        return select_from_menu(header, question, options)

    def menu_get_existing_customer_yes_no(self):
        '''
        Collect user's selection: Existing Customer Yes/No 
        ''' 
        header = "         Open a new account              "
        question = "Are you an existing customer?"
        options = (("Yes", Bank.YES),
                   ("No", Bank.NO))
        
        return select_from_menu(header, question, options)

    def menu_get_new_account_type(self):
        '''
        Collect user's selection from account type menu.
        ''' 
        question = "Which type of account would you like to open?"
        options = (("Checking Account", CheckingAccount),
                   ("Savings Account", SavingsAccount))

        return select_from_menu("", question, options)

    def menu_get_available_transactions(self,transaction_metadata):
        '''
        Collect user's selection from available transactions menu
        '''
        header = ""
        question = "Available transactions"
        options = [(transaction_metadata[meta][0], meta)
                   for meta in transaction_metadata]  # (display_name, method)

        return select_from_menu(header, question, options)
    
    def get_new_customer(self):
        '''
        Interact with the user to collect necessary infomation.  Return the new customer or raise an exception if the customer already exists
        or there are validation errors.
        '''
        customer = Customer()
        info_metadata = customer.get_info_metadata()
        info_metadata_parameters = info_metadata['set_info'][1]
        kwargs = collect_metadata_kwargs(info_metadata_parameters)
        customer.set_info(**kwargs)

        if customer in self.customers.values():    # customer equality based on first_name, last_name ssn
            raise self.CustomerAlreadyExistsException
        else:
            # add to working dictionary
            self.customers[customer.id] = customer
            print("\nCongratulations, You are our new customer! Your customer id is: {n}.".format(
                n=customer.id))
            print("\nPlease remember this id and your pin for future transactions.")
            input("\nPlease hit return to open your new account")
            return customer

    def get_validated_customer(self):
        '''
        Returns customer or raises exception
        '''
        option = self.menu_get_existing_customer_yes_no()
        if option == Bank.YES:
            print("")
            customer_id = input("Please enter your customer id: ").strip()
            pin = input("Please enter your pin: ").strip()
            customer = self.customers.get(customer_id)
            if customer == None or customer.pin != pin:
                raise self.InvalidCredentialsException
            return customer
        elif option == Bank.NO:
            print("\nOK.  Let's sign you up with the following information\n")
            return self.get_new_customer()
        else:
            raise self.BankSystemError("get_validated_customer: Received answer other than Yes/No")

    def get_new_account(self):

        customer = self.get_validated_customer()
        account_type = self.menu_get_new_account_type()
        account = account_type(customer_id = customer.id)
        
        open_metadata = account.get_open_metadata()
        open_metadata_parameters = open_metadata['open'][1]
        kwargs = collect_metadata_kwargs(open_metadata_parameters)
        account.open(**kwargs)

        self.accounts[account.id] = account
        customer.add_account(account.id)
        
        input(
            "Congratulations! Your account {0} has been opened. " 
            "Remember this account number for future transactions.\n\n"
            "Please hit return to continue".format(account.id))

    def get_validated_account(self):

        # look for id in accounts dictionary and then check pin
        account_id = input("\nPlease enter your account id ").strip()
        pin = input("\nPlease enter your PIN ").strip()

        account = Bank.accounts.get(account_id)
        if account:
            customer = self.customers[account.customer_id]
            if pin == customer.pin:
                return account

        raise self.InvalidCredentialsException

    def run_transaction(self):

        account = self.get_validated_account()
        customer = self.customers[account.customer_id]

        print('\033c', end='')  # clear screen
        print(f"Hi, {customer.first_name}. Welcome Back!")
        another_transaction = Bank.YES

        while another_transaction == Bank.YES:

            transaction_metadata = account.get_transaction_metadata()
            transaction_method = self.menu_get_available_transactions(transaction_metadata)  # pick desired method from menu
            transaction_parameters = transaction_metadata[transaction_method][1]
            kwargs = collect_metadata_kwargs(transaction_parameters)

            try:
                getattr(account, transaction_method)(**kwargs)                                #   call method
                print("\nCongratulations. Transaction completed successfully.\n")
                print(account.status())                
            except TransactionFailedException as ex:
                print("\nTransaction failed.")
                print(ex)

            input("\nPlease hit return to continue")            
            question = f'Would you like to perform another transaction on this account, {customer.first_name}?'
            options = (("Yes", Bank.YES),("No", Bank.NO))
        
            another_transaction = select_from_menu("", question, options)

    def run(self):
        while True:
            try:
                activity = self.menu_get_main_activity()
                if activity == Bank.RUN_TRANSACTION:
                    self.run_transaction()
                elif activity == Bank.OPEN_NEW_ACCOUNT:
                    self.get_new_account()
                elif activity == Bank.QUIT:
                    print("\nThank you for visiting us.  Have a great day!")
                    break
                else:
                    raise Bank.BankSystemError("Unexpected value from main menu")                  

            except Bank.InvalidCredentialsException:
                input("Logon failed. Invalid credentials.  Please hit return to continue")
            except Bank.CustomerAlreadyExistsException:
                input("Login Failed. Customer already exists.  Please hit return to continue")
            except Exception as ex:
                print(ex)
                input("Unexpected error.  Please hit return to continue")

def __main__():
    Bank().run()

if __name__ == "__main__":

    Bank().run()