from customer import Customer, CustomerAlreadyExistsException
from account import Account, TransactionFailedException, CheckingAccount, SavingsAccount
# from bankutils import select_from_menu


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

    class AccountValidationException(Exception):
        pass

    class InvalidCredentialsException(Exception):
        pass

    class BankSystemError(Exception):
        pass 

    def persist(self):
        pass

    def get_activity_from_main_menu(self):
        '''
        Collect user's selection from main menu.
        ''' 
        header = "     Welcome to Simple Friendly Bank     "
        question = "What would you like to do?"
        options = (("Open a new account", Bank.OPEN_NEW_ACCOUNT),
                   ("Access an existing account", Bank.RUN_TRANSACTION),
                   ("Quit", Bank.QUIT))

        return select_from_menu(header, question, options)

    def get_yes_no_existing_customer(self):
        '''
        Collect user's selection: Existing Customer Yes/No 
        ''' 
        header = "         Open a new account              "
        question = "Are you an existing customer?"
        options = (("Yes", Bank.YES),
                   ("No", Bank.NO))
        
        return select_from_menu(header, question, options)

    def get_new_account_type(self):
        '''
        Collect user's selection from account type menu.
        ''' 
        header = ""
        question = "Which type of account would you like to open?"
        options = (("Checking Account", Account.CHECKING),
                   ("Savings Account", Account.SAVINGS))

        return select_from_menu(header, question, options)

    def get_transaction_method(self,transaction_metadata):
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

        print("")
        print("OK.  Let's sign you up with the following information\n")

        info_metadata = customer.get_info_metadata()
        info_metadata_parameters = info_metadata['set_info'][1]
        kwargs = {parm: input(text) for parm, text in info_metadata_parameters}
        customer.set_info(**kwargs)

        if customer in self.customers.values():    # customer equality based on first_name, last_name ssn
            raise CustomerAlreadyExistsException
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
        option = self.get_yes_no_existing_customer()
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
            raise self.BankSystemError("get_validated_customer: Received answer other than Yes/No")

    def get_new_account(self):

        customer = self.get_validated_customer()
        type = self.get_new_account_type()
        if type == Account.CHECKING:
            account = CheckingAccount(customer.id)
        if type == Account.SAVINGS:
            account = SavingsAccount(customer.id)
        open_metadata = account.get_open_metadata()
        open_metadata_parameters = open_metadata['open'][1]
        kwargs = {parm: input(text) for parm, text in open_metadata_parameters}
        account.open(**kwargs)

        self.accounts[account.id] = account
        customer.add_account(account.id)
        self.persist()
        input(
            "Congratulations! You're account {0} has been opened. " 
            "Remember this account number for future transactions.\n"
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
        print("Hi, {0}. Welcome Back!".format(customer.first_name))
        transaction_metadata = account.get_transaction_metadata()
        transaction_method = self.get_transaction_method(
            transaction_metadata)  # pick desired function from menu
        transaction_parameters = transaction_metadata[transaction_method][1]
        kwargs = {parm: input(text) for parm, text in transaction_parameters}
        getattr(account, transaction_method)(
            **kwargs)                           # call method

        input("Congratulations. Transaction completed successfully.  Please hit return to continue")

    def run(self):
        while True:
            try:
                activity = self.get_activity_from_main_menu()
                if activity == Bank.RUN_TRANSACTION:
                    self.run_transaction()
                elif activity == Bank.OPEN_NEW_ACCOUNT:
                    self.get_new_account()
                elif activity == Bank.QUIT:
                    print("\nThank you for visiting us.  Have a great day!")
                    break
                else:
                    print("\nSystem Error")
                    break
            # handle all exceptions  here
            except Bank.InvalidCredentialsException:
                input("Invalid credentials.  Please hit return to continue")

            except Exception as ex:
                print(ex)
                input("error message.  Please hit return to continue")

if __name__ == "__main__":

    Bank().run()