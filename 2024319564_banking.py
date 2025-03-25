import json
import random
from datetime import datetime


#what should json file be called, what can be in there
#person: username, password, pin, bank account number, current balance
    #transactions: transaction type, time, amount
        #transfer needs from and to (username)

#checks if username is taken, return false if it is. otherwise true
#this can be used to check if username is valid!! just opposite
def username_check(input_username):
    #load usernames from users.json
    with open('users.json', 'r') as file:
        data = json.load(file)
    #check if username is already taken
    users = data.get("users", [])
    usernames = [username["username"] for username in users]
    if input_username in usernames:
        return False
    return True

#takes username as input, checks if valid. if it is -> load it to users.data
def register_get_username():
    username = input("--> ")
    #username = input("Input desired username")
    if not username_check(username):
        print("The username is already taken.")
        register_main()
    #load to users.json file, download the users first, then add it and dump it. seems a bit redundant
    else:
        return username

#must be over 7 letters, at least one capital letter, and one special character
def check_password(password):
    special_characters = ["!", "@", "#", "$", "%", "^" , "&", "*", "(", ")"]
    #is set to one if long enough
    is_long_enough = True if len(password) > 7 else False
    #if password has special character, this will be set to 1
    has_special_character = False
    has_capital_letter = False
    for letter in password:
        if letter in special_characters:
            has_special_character = True
        if letter.isupper():
            has_capital_letter = True
    if not is_long_enough:
        print("Password is too short. Must be at least 8 characters")
    if not has_special_character:
        print("Password does not have mandatory special character\nMust consist one of ! @ # $ ^ & * ( )")
    if not has_capital_letter:
        print("The password needs to have at least one capital letter")
    #returns true if password is approved, otherwise false
    if is_long_enough and  has_special_character and has_capital_letter:
        return True
    return False
    
    
def register_create_password():
    password = input("--> ")
    if check_password(password):
        return password
    #restart whole register process
    else: 
        print(f'{"-"*20}')
        register_main()

#checks if pin is valid, returns true if it is, false if not
def register_validate_pin(pin):
    for p in pin:
        if not p.isdigit():
            return False
    return False if len(pin) != 4 else True
    
#takes pin input from user in register phase 
def register_get_pin():
    pin = input("--> ")
    if register_validate_pin(pin):
        return pin 
    else: #restart whole register process
        print("The pin you provided was not valid. It gotta be a 4 digit number")
        register_main()



def register_main():
    #username gets put in users.json, but i will also create a json for every user.
    print(f'{"#"*10} REGISTER {"#"*10}')
    print("Input desired username: ")
    username = register_get_username()
    print("Type in your desired password. Password must conist of at least 8 charachter,\nInclude one of these special characters ! @ # $ ^ & * ( ),\nAnd have at least one capital letter")
    password = register_create_password()
    print("Choose a 4 digit PIN password: ")
    pin_password = register_get_pin()
     #create 5 digit random bank account number, can be anything between 0 and 99999. 
    bank_account_number = f"{random.randint(0, 99999):05d}"
    #load username to users.json
    with open('users.json', 'r') as file:
        data = json.load(file)
        users = data.get("users", [])
        users.append({"username": username, "account_number": bank_account_number, "password":password,"pin":pin_password, "account_number":bank_account_number, "balance":100})
        data["users"] = users
        with open('users.json', 'w') as file:
            json.dump(data, file, indent=4)
        
    #add user to the transactions (history) file
    with open('transactions.json', 'r') as transaction_file:
        data = json.load(transaction_file)
        transactions = data.get("transactions", {})
        # transactions[username] = {"history": []}
        transactions[username] = {"history": []}
        data["transactions"] = transactions
        with open('transactions.json', 'w') as transaction_file:
            json.dump(data, transaction_file, indent=4)
    #create new json file for this user, have to add transactions later
    # user_json = {"password":password, "pin":pin_password, "account_number":bank_account_number, "balance": 100, "history": []}
    # #serializes python dict to json format
    # json_data = json.dumps(user_json)
    # #creates new file in form username.json
    # with open(f'{username}.json', 'w') as user_file:
    #     user_file.write(json_data)

    #go back to "start" screen
    initialize()

#check that input is a digit between 1 and 5
def main_chosen_menu():
    valid = ['1', '2', '3', '4', '5']
    while True:
        user_input = input("Choose menu: ")
        if user_input in valid and user_input.isdigit():
            return user_input
        print("Input was not valid")


#checks if pin is the same as PIN in 'username'.json file
def check_pin(username, pin):
    # with open (f'{username}.json', "r") as file:
    #     data = json.load(file)
    return True if pin == username["pin"] else False


#check if its not to much money, if so -> withdraw and update json file. Create timestamp
def withdraw_money(username, money_to_withdraw):
    # if not money_to_withdraw.isdigit():
    #     print("'Amount' was not a valid digit")
    #     main_screen(username)
    #     return
    #load users balance
    with open ('users.json', "r") as file:
        data = json.load(file)
    users = data.get("users", [])
    user = next((user for user in users if user["username"] == username), None)
    balance = int(user.get("balance"))
    #if enough money
    if int(money_to_withdraw) <= balance:
        balance -= int(money_to_withdraw)
        #now update json file
        user["balance"] = balance
        with open('users.json', "w") as file:
            json.dump(data, file, indent=4)
        #create timestamp
        #history_list = data["history"]
        with open("transactions.json", "r") as trans_file:
            data = json.load(trans_file)
        transactions = data.get("transactions")
        history_list = transactions[username].get("history")
        history_list.append({"timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "type": "withdrawn", "amount":money_to_withdraw})
        transactions[username] = history_list
        with open ('transactions.json', "w") as f:
            json.dump(data, f, indent=4)
        print(f'{"-"*10} WITHDRAWING SUCESSFUL {"-"*10}')
    else:
        print("You do not have the sufficient amount on your account")
        return

def withdraw_main(username):
    print(f'{"#"*10} WITHDRAWING {"#"*10}')
    with open ('users.json', "r") as file:
        data = json.load(file)
    users = data.get("users", [])
    user = next((user for user in users if user["username"] == username))
    #print info
    print("Username: " , username)
    print("Balance: ", user["balance"])
    print("Account number: ", user["account_number"])
    print(f'{"-"*20}')
    money_to_withdraw = input("How much money do you want to withdraw? \n--> ")
    input_pin = input("Input PIN to withdraw \n--> ")
    #check if pin is correct, if so -> call on function to withdraw money
    tests = 0
    if not money_to_withdraw.isdigit():
        print("'Amount' was not a valid digit")
        tests+=1
    if not check_pin(user, input_pin):
        print("PIN was wrong")
        tests+=1
    if(tests == 0):
        withdraw_money(username, money_to_withdraw)
        main_screen(username)
    else:
        main_screen(username)


def deposit_money(user, money_to_deposit, data):
    if not money_to_deposit.isdigit():
        print("'Amount' was not a valid digit")
        main_screen(user["username"])
    else:
        #load users balance
        balance = int(user.get("balance"))
        balance += int(money_to_deposit)
        user["balance"] = balance
        with open ('users.json', 'w') as file:
            json.dump(data, file, indent=4)
        
        #write to transactions.json
        with open("transactions.json", "r") as trans_file:
            data = json.load(trans_file)
        username = user["username"]
        transactions = data.get("transactions")
        history_list = transactions[username]
        history_list.append({"timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "type": "deposit", "amount":money_to_deposit})
        transactions[username] = history_list
        with open ('transactions.json', "w") as f:
            json.dump(data, f, indent=4)
        print(f'{"-"*10} DEPOSIT SUCESSFUL {"-"*10}')




def deposit_main(username):
    print(f'{"#"*10} DEPOSIT {"#"*10}')
    with open ('users.json', "r") as file:
        data = json.load(file)
    users = data.get("users", [])
    user = next(user for user in users if user["username"] == username)
    #print info
    print("Username: " , username)
    print("Balance: ", user["balance"])
    print("Account number: ", user["balance"])
    print(f'{"-"*20}')
    money_to_deposit = input("How much money do you want to deposit? \n--> ")
    input_pin = input("Input PIN to deposit\n-->  ")
    #check if pin is correct, if so -> call on function to withdraw money
    tests = 0
    if not money_to_deposit.isdigit():
        print("Amount was not a valid digit")
        tests+=1
    if not check_pin(user, input_pin):
        print("PIN was wrong")
        tests+=1
    if(tests==0):
        deposit_money(user, money_to_deposit, data)
        main_screen(username)
    else:
        main_screen(username)
#takes bank account number, if it finds it in the users.json file it returns the username
def fetch_data_transfer_to(account_number):
    if len(account_number) == 5 and account_number.isdigit():
        with open ("users.json", 'r') as file:
            data = json.load(file)
        users = data.get("users")
        for user in users:
            if(user["account_number"] == account_number):
                return user["username"]
        print("Couldnt find the bank account")
        return None
    else:
        print("Account number was not valid")
        return None


def transfer_logic(money_to_transfer, user_from, user_to, users_data):
    #first check if the from user has the sufficient amount, then perform the logic
    if not money_to_transfer.isdigit():
        print("'Amount' was not a valid digit")
        main_screen(user_from["username"])
        return
    
    balance = int(user_from["balance"])

    #first check if user got enough money, then subtract it and create timestamp. Load all to json file
    if int(money_to_transfer) > balance:
        print("You do not have the sufficient amount on your account")
        return
    else:
        #subtract from user_from, add to user_to and update json file
        balance -= int(money_to_transfer)
        user_from["balance"] = balance
        balance_user_to = int(user_to["balance"])
        balance_user_to += int(money_to_transfer)
        user_to["balance"] = balance_user_to
        with open('users.json', 'w') as file:
            json.dump(users_data, file, indent=4)
        #create timestamp
        with open('transactions.json', 'r') as file:
            data = json.load(file)
        transactions = data.get("transactions")
        history_list = transactions[user_from["username"]]
        history_list.append({"timestamp":datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "type": "transfer", "amount":money_to_transfer, "from": user_from["username"], "to": user_to["username"]})
        transactions[user_from["username"]] = history_list
        with open ('transactions.json', "w") as f:
            json.dump(data, f, indent=4)
        print(f'{"-"*10} TRANSFER SUCESSFUL {"-"*10}')
        

#uses other function to find "to" s json file
def transfer_main(username):
    print(f'{"#"*10} TRANSFER {"#"*10}')
    with open ( 'users.json', "r") as file:
        users_data = json.load(file)
    users = users_data.get("users")
    user_from = next(user for user in users if username == user["username"])
    #print info
    print("Username: " , username)
    print("Balance: ", user_from["balance"])
    print("Account number: ", user_from["account_number"])
    print(f'{"-"*20}')
    #ask user for account number they want to transfer to. 
    transfer_to = input("Account number you want to transfer to\n--> ")
    money_to_transfer = input("How much money do you want to deposit?\n--> ")
    input_pin = input("Input PIN to deposit: \n--> ")
    username_to = fetch_data_transfer_to(transfer_to)
    if username_to is not None:
        user_to = next(user for user in users if username_to == user["username"])
    #will be none if it couldnt find the user
    if not check_pin(user_from, input_pin):
        print("PIN was wrong")
        main_screen(username)
    elif username_to == None:
        main_screen(username)
    else:
        transfer_logic(money_to_transfer, user_from, user_to, users_data)
        main_screen(username)
        


#print for withdrawings. 
def print_withdrawn_history(transaction):
    print(f'Type: Withdrawing\nTime: {transaction["timestamp"]}\nAmount: {transaction["amount"]}\n{"-"*20}')

#print for deposit
def print_deposit_history(transaction):
    print(f'Type: Deposit\nTime: {transaction["timestamp"]}\nAmount: {transaction["amount"]}\n{"-"*20}')

#print for transfer
def print_transfer_history(transaction):
    print(f'Type: Transfer\nTime: {transaction["timestamp"]}\nFrom: {transaction["from"]}\nTo: {transaction["to"]}\nAmount: {transaction["amount"]}\n{"-"*20}')

#reverse list to get the newest transactions first
def show_history_main(username):
    print(f'{"#"*10} HISTORY {"#"*10}')
    with open ('transactions.json', "r") as file:
        data = json.load(file)
    transactions = data["transactions"]
    history_list = transactions[username]
    sorted_history = reversed(history_list)
    #sorted_history = reversed(data["history"])
    for transaction in sorted_history:
        if transaction["type"] == "withdrawn":
            print_withdrawn_history(transaction)
        elif transaction["type"] == "deposit":
            print_deposit_history(transaction)
        elif transaction["type"] == "transfer":
            print_transfer_history(transaction)
    main_screen(username)

    

#must always show username, current balance, and bank account number. Ask user too choose from menu
def main_screen(username):
    #download json
    print(f'{"#"*10} MAIN SCREEN {"#"*10}')
    with open ('users.json', "r") as file:
        data = json.load(file)
        users = data.get("users", [])
        for user in users:
            if user["username"] == username:
                #print info
                print("Username: " , username)
                print("Balance: ", user["balance"])
                print("Account number: ", user["account_number"])
                print(f'{"-"*20}')
                print("1. History\n2. Withdraw\n3. Deposit\n4. Transfer\n5. Logout ")
                chosen_menu = main_chosen_menu()

    if chosen_menu == '1':
        show_history_main(username)
    #withdraw
    elif chosen_menu == '2':
        withdraw_main(username)
    elif chosen_menu == '3':
        deposit_main(username)
    elif chosen_menu == '4':
        transfer_main(username)
    elif chosen_menu == '5':
        initialize()




#go in username.json and see if its the correct password. Return true if so
def login_check_password(username, password):
    with open('users.json', "r") as file:
        data = json.load(file)
        users = data.get("users", [])
        for user in users:
            if user["username"] == username:
                json_password = user["password"]
    return True if password == json_password else False
    

#if wrong, return to home (initialize) screen. Mostly because of if there is no accounts theres no reason to keep trying
def login_main():
    print(f'{"#"*10} LOGIN {"#"*10}')
    username = input("Type in your username: ")
    password = input("Type in your password: ")
    #was used for checkingif username is already taken, so see if false in this case
    if username_check(username) or not login_check_password(username, password):
        print("Username or password is invalid")
        initialize()
        
    else:
        main_screen(username)

    
#check if customer chose a number between 1 and 3
def check_chosen_menu_initialize(chosen_menu):
    if chosen_menu.isdigit() and chosen_menu in ["1", "2", "3"]:
        return True
    return False

#first page user sees. Chooses if they want to register, login or exit
def initialize():
    print(f'{"#"*10} HOME PAGE {"#"*10}')
    chosen_menu = (input("1. Register\n2. Login\n3. Exit\nChoose menu: "))
    #check validity of input
    if check_chosen_menu_initialize(chosen_menu) == False:
        print("You have to choose a menu that I provided")
        initialize()
    else:
        if(chosen_menu == "1"):
            register_main()
        elif(chosen_menu == '2'):
            login_main()
        else: exit()

if __name__=="__main__":
    initialize()
