class Account():
    ACCOUNT_TYPES = ['CHECKING', 'SAVINGS']



class SavingsAccount(Account):

    SAVINGS_ID_PREFIX = "SAV"
    pass
class CheckingAccount(Account):
    CHECKING_ID_PREFIX = "CHK"
    pass

    def order_checks(self):
        pass

