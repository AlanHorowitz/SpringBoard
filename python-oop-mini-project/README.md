## simplefriendlybank 

### This project simulates transactions with Simple Friendly Bank via a menu driven user interface.

### The bank is modeled by three classes:  Bank, Customer and Account.  A Bank may have one or many Customers and a Customer may have one or many Accounts.   The Accounts that a Customer may open are CheckingAccount and SavingsAccount, which are subclasses of Account.  To open an account, you must first register as a customer and select a personal identification number (PIN).  You will be issued customer and account ids for future use.

### Please see class diagram at uml.jpg

### The type of transactions supported by the accounts are:

### SavingAccount
* deposit
* withdrawal

### CheckingAccount
* deposit
* write check
* order new checks

### Account status information is displayed after each transaction completes.

### This project requires Python 3 and is launched using the following command in this directory

```
python -m simplefriendlybank
```
### which displays the welcome menu
```
-----------------------------------------
     Welcome to Simple Friendly Bank     
-----------------------------------------

What would you like to do?

[1] Open a new account
[2] Access an existing account
[3] Quit

Please select an option from the menu:
```
### Open an account and happy banking!