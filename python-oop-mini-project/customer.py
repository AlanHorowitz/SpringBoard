class CustomerAlreadyExistsException(Exception):
    pass

class Customer():

    CUSTOMER_ID_PREFIX = "CUST"

    def __init__(self, id):
        self._customer_id = Customer.CUSTOMER_ID_PREFIX + str(id)
        accounts = []

    def __eq__(self, other):
        if isinstance(other, Customer):
            if self.first_name == other.first_name and
               self.last_name == other.last_name and
               self.ssn == other.ssn:
                    return True
        return False
             
    def add_account(self, account):
        accounts.append(account)
        
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
