class CustomerAlreadyExistsException(Exception):
    pass


class Customer:

    CUSTOMER_ID_PREFIX = "CUST"
    next_customer_id = 1

    def __init__(self):

        self._id = Customer.CUSTOMER_ID_PREFIX + str(Customer.next_customer_id)
        self._accounts = []

        self._first_name = ""
        self._last_name = ""
        self._social_security_number = ""
        self._street_address = ""
        self._state = ""
        self._zip_code = ""
        self._pin = ""

        Customer.next_customer_id += 1

    def get_info_metadata(self):

        return {
            "set_info": (
                "No Display",
                [
                    ("first_name", "Please enter your first name: ", "string"),
                    ("last_name", "Please enter your last name: ", "string"),
                    (
                        "social_security_number",
                        "Please enter your social security number: ",
                        "string",
                    ),
                    (
                        "pin",
                        "Please enter your personal identification number: ",
                        "string",
                    ),
                ],
            )
        }

    def set_info(self, **kwargs):

        self._first_name = kwargs.get("first_name")
        self._last_name = kwargs.get("last_name")
        self._social_security_number = kwargs.get("social_security_number")
        self._pin = kwargs.get("pin")

    @property
    def id(self):
        return self._id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def social_security_number(self):
        return self._social_security_number

    @property
    def pin(self):
        return self._pin

    def add_account(self, account_id):
        self._accounts.append(account_id)

    def __eq__(self, other):
        if isinstance(other, Customer):
            if (
                (self.first_name == other.first_name)
                and (self.last_name == other.last_name)
                and (self.social_security_number == other.social_security_number)
            ):
                return True
        return False
