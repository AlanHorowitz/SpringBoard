class CustomerAlreadyExistsException(Exception):
    pass

class Customer():

    def __init__(self, first_name=None, last_name=None, social_security_number=None):
        self._first_name = first_name
        self._last_name = last_name
        self.ssn = social_security_number
        
    def add_account(self):
        pass
    def load_customer(self):
        '''
        Retrieve customer from persistence 
        '''
        pass

    def get_validation_parameters(self):
        self.first_name = input("\nYour first name            : ") 
        self.last_name =  input("\nYour last name             : ")     
        self.ssn =        input("\nYour social security number: ")   

    def get_other_parameters(self):
        self.street_address = input("\nYour street address        : ") 
        self.state =          input("\nYour state                 : ")     
        self.zip_code=        input("\nYour zip code              : ")
        self.pin =            input("\n\nNow, choose a personal identification number: ")

class Bank():

    customers = {}
    accounts = {}
    next_customer_id = 1

    pass

    def has_customer(self, first_name, last_name, ssn):
        return False

    def create_new_customer(self):
        '''
        Interact with the user to collect customer infomation.  Raise a CustomerAlreadyExists exception, if there is a customer
        with the same first_name, last_name and ssn.
        '''
        cust = Customer()
        
        cust.get_validation_parameters()
        if cust in self.customers.values():   # override __eq__
            raise CustomerAlreadyExistsException
        cust.get_other_parameters()
        cust.customer_id = "CUST" + str(self.next_customer_id)
        assert(self.customers.get(cust.customer_id) == None)
        self.customers[cust.customer_id] = cust
        self.next_customer_id += 1

        return cust
    
    def persist_customers(self):
        pass
