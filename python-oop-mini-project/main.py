from banking import Bank
from banking import CustomerAlreadyExistsException

#  Deal with the terminal user
# high level screens (interface navigation) can run in common loop, but Customers and Accounts collect their own information for the user

def welcome_screen():
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
            return new_account_screen
        elif s == "2":
            return existing_account_screen
        elif s == "3":
            return None
    

def new_account_screen():
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
        if s == "2":
            try:  
                cust = bank.create_new_customer()  
                print("\nCongratulations, You are our new customer! Your customer id is: {n}.".format(n=cust.customer_id)) 
                print("\nPlease remember this id and your pin for future transactions.\n\nPress enter to continue")
            except(CustomerAlreadyExistsException):
                print("\nCustomer was a duplicate and could not be added.\n\nPress enter to continue")
                
            input()
            return new_account_screen

        elif s == "1":
            print("\nOK, Let's create your new account")
            customer_id = input("\nPlease enter your customer id")
            customer_pin = input("\nPlease enter your pin")
            if bank.check_credentials(customer_id, customer_pin):
                # what kind of account do you want to open?
                new_account = bank.create_new_account(customer_id)
                new_account.get_options()
            else:
                pass

            return new_account_screen
        elif s == "3":
            return welcome_screen

    return welcome_screen

def existing_account_screen():
    print("Existing Account Screen")
    try:
        acct = bank.get_validated_account()
        option = acct.get_options()
        transaction_data = option.get_transaction_data()
        acct.run_transaction(option, transaction_data)
    except Bank.AccountVaidationError:
        print("bad account number or id")
    return welcome_screen

if __name__ == '__main__':

    bank = Bank()

    # bank open
    # bank printtransaction
    #  bank.close
    # bank.inventory
    next = welcome_screen
    
    # process screens until done
    while next:
        print('\033c', end='')  # clean screen
        next = next()
    print("\nThank you for visiting us.  Have a great day!")