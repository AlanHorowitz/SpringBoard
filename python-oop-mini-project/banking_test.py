from banking import Bank
from banking import Customer
from banking import CustomerAlreadyExistsException

def test_1():
    cust = Customer()
    cust.get_validation_parameters()
    print(cust)