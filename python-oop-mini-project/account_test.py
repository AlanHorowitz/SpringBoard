from account import Account, SavingsAccount, CheckingAccount, TransactionFailedException

import pytest

def test_open():
    a = Account()
    assert a._balance == 0

    c1 = CheckingAccount()
    assert c1._balance == 0
    # test defaults
    c1.open()
    assert c1._balance == 100
    assert c1._remaining_checks == 10

    c2 = CheckingAccount()
    assert c2._id == "CHK2"
    c2.open(opening_balance=50, number_starter_checks=5)
    assert c2._balance == 50
    assert c2._remaining_checks == 5

    s1 = SavingsAccount()
    assert s1._balance == 0
    # test defaults
    s1.open()
    assert s1._balance == 100
    
    s2 = SavingsAccount()
    assert s2._id == "SAV2"
    s2.open(opening_balance=50)
    assert s2._balance == 50

def test_open_with_customer_id():

    c1 = CheckingAccount("CUST1")
    assert c1._customer_id == "CUST1"

    s1 = SavingsAccount("CUST2")
    assert s1._customer_id == "CUST2"

def test_withdrawal():

    s1 = SavingsAccount()
    s1.open(opening_balance=50.)
    s1.withdraw(withdrawal_amount=20.)
    assert s1._balance == 30.
    s1.withdraw(withdrawal_amount=20.)
    assert s1._balance == 10.
    with pytest.raises(TransactionFailedException):
        s1.withdraw(withdrawal_amount=20.)
    assert s1._balance == 10.

    