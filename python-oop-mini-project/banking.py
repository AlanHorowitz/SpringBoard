from customer import Customer, CustomerAlreadyExistsException

class Bank():

    customers = {}
    accounts = {}
    next_customer_id = 1
    
    def welcome_screen(self):
        print("-----------------------------------------")
        print("     Welcome to Simple Friendly Bank     ")
        print("-----------------------------------------")
        print("")
        print("What would you like to do?")
        print("")
        print("[1] Open a new account" )
        print("[2] Access an existing account")
        print("[3] Quit")
        print("")

        s = ""
        while s != "3":
            print("Please Enter from menu. Use [3] to quit: ", end='')
            s = input().strip()
            if s == "1":
                return self.new_account_screen 
            elif s == "2":
                return self.existing_account_screen
            elif s == "3":
                return None
                
    def new_account_screen(self):
        print("-----------------------------------------")
        print("         Open a new account              ")
        print("-----------------------------------------")
        print("")
        print("Are you an existing customer?")
        print("")
        print("[1] Yes" )
        print("[2] No")
        print("[3] Quit")
        print("")

        s = ""
        while s != "3":

            print("Please Enter from menu. Use [3] to quit: ", end='')
            s = input().strip()

            if s == "1":

                print("\nOK, Let's create your new account")
                customer_id = input("\nPlease enter your customer id")
                customer_pin = input("\nPlease enter your pin")
                try:
                    cust = self.validate_customer_credentials(customer_id, customer_pin)
                    acct = self.create_new_account(cust)
                    print("\nCongratulations, Your new {type} account has been created! Your account id is {id}.".format(n=cust.customer_id)) 
                    print("\nPlease remember this id and your pin for future transactions.")
                    next_screen = self.welcome_screen
                except(self.InvalidCredentialsException):
                    print("\nPin is not valid for customer id {n}. ".format(n=cust.customer_id))
                    next_screen = self.new_account_screen 
                    pass

                input("\n\nPress enter to continue ")
                return next_screen

            elif s == "2":

                try:  
                    cust = self.create_new_customer()  
                    print("\nCongratulations, You are our new customer! Your customer id is: {n}.".format(n=cust.customer_id)) 
                    print("\nPlease remember this id and your pin for future transactions.")
                    next_screen = self.welcome_screen

                except(CustomerAlreadyExistsException):
                    print("\nCustomer was a duplicate and could not be added.")
                    next_screen = self.new_account_screen
                    
                input("\n\nPress enter to continue ")
                return next_screen
            
            elif s == "3":
                return self.welcome_screen

    def existing_account_screen(self):
        print("Existing Account Screen")
        try:
            acct = self.get_validated_account()
            option = acct.get_options()
            transaction_data = option.get_transaction_data()
            acct.run_transaction(option, transaction_data)

        except self.AccountValidationError:
            print("bad account number or id")

        except self.TransactionFailedError:
            print("bad account number or id")

        return self.welcome_screen

    class InvalidCredentialsException(Exception):
        pass

    def run(self):

        next = self.welcome_screen    
        # process screens until done
        while next:
            print('\033c', end='')  # clean screen
            next = next()
        print("\nThank you for visiting us.  Have a great day!")

    def has_customer(self, first_name, last_name, ssn):
        return False

    def create_new_customer(self):
        '''
        Interact with the user to collect customer infomation.  Raise a CustomerAlreadyExists exception, if there is a customer
        with the same first_name, last_name and ssn.
        '''
        cust = Customer(self.next_customer_id)
        
        cust.get_validation_parameters()
        if cust in self.customers.values():    # customer equality based on valuation parameters
            raise CustomerAlreadyExistsException
        cust.get_other_parameters()
        assert(self.customers.get(cust.customer_id) == None)
        self.customers[cust.customer_id] = cust
        self.next_customer_id += 1

        return cust

    def create_new_account(self, cust):
        
        acct = Account.create_new_account(cust, self.next_account_id)
        # add to list
        pass

    def validate_customer_credentials(self, customer_id, customer_pin):
        '''
        return validated Customer or raise InvalidCredentialsException
        '''
        cust = self.customers.get(customer_id)
        if cust == None or cust.customer_pin != customer_pin.strip():
            raise self.InvalidCredentialsException 
        return cust
    
    def validate_account_credentials(self, account_id, customer_pin):
        pass

    def persist_customers(self):
        pass
