from customer import Customer

def test_new():

    a = Customer()
    assert  a.id == "CUST1"
    b = Customer()
    assert b.id == "CUST2"

def test_set_info():

    a = Customer()
    m = a.get_info_metadata()
    kwargs = { tup[0] : "Val" + str(i) for i, tup in enumerate(m['set_info'][1])}
    a.set_info(**kwargs)
    assert a._first_name == "Val0"
    assert a._last_name == "Val1"
    assert a._social_security_number == "Val2"
    assert a._pin == "Val3"

def test_equality():

    a = Customer()
    b = Customer()
    c = Customer()
    d = Customer()

    a.set_info(first_name="Bob", last_name="Jones", social_security_number='123', pin='555')
    b.set_info(first_name="Bob", last_name="Jones", social_security_number='456', pin='555')
    c.set_info(first_name="Bob", last_name="Jones", social_security_number='123', pin='666')
    d.set_info(first_name="Bob", last_name="Smith", social_security_number='123', pin='666')
    assert a != b
    assert a == c
    assert b != c
    assert a != d

def test_add_account():

    a = Customer()
    a.add_account("ACCT1")
    a.add_account("ACCT2")
    assert a._accounts == ["ACCT1", "ACCT2"]

def test_properties():

    Customer.next_customer_id = 10
    a = Customer()
    a.set_info(first_name="Bob", last_name="Jones", social_security_number='123', pin='555')
    assert a.id == "CUST10"
    assert a.first_name == "Bob"
    assert a.last_name == "Jones"
    assert a.social_security_number == "123"
