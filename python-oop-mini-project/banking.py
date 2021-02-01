class Customer():

    def __init__(self, first_name=None, last_name=None, social_security_number=None):
        self._first_name = first_name
        self._last_name = last_name
        self.ssn = social_security_number
        
    def add_account():
        pass
    def load_customer():
        '''
        Retrieve customer from persistence 
        '''
        pass


class Bank():
    pass

    def has_customer(self, first_name, last_name, ssn):
        return False

    def create_new_customer(self,first_name, last_name, ssn):
        return Customer(first_name, last_name, ssn)
    
    def persist_customers(self):
        pass
