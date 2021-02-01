from banking import Bank

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
            print("\nGreat, Let's sign you up. We need just a little information. Please enter the following:")
            first_name = input("\nYour first name            : ") 
            last_name =  input("\nYour last name             : ")     
            ssn =        input("\nYour social security number: ")    
            if bank.has_customer(first_name, last_name, ssn):
                print("\nYou are an existing customer! Press enter to continue")
                input()
                return new_account_screen
            else:
                new_cust = bank.create_new_customer(first_name, last_name, ssn)
                new_cust.street_address = input("\nYour street address        : ") 
                new_cust.state =          input("\nYour state                 : ")     
                new_cust.zip_code=        input("\nYour zip code              : ")
                new_cust.pin =            input("\n\nNow, choose a personal identification number: ")
                bank.persist_customers()
                print("\nCongratulations, You are our new customer! Your customer id is: {n}.".format(n='1')) 
                print("\nPlease remember this id and your pin for future transactions.\n\nPress enter to continue")
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