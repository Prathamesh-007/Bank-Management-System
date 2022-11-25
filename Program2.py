from getpass import getpass
import SQL_Control_Functions as SCF


def CreateAccount():
    cust_id=int(input("Enter Customer ID: "))
    if SCF.CheckCustomer(mydb, cust_id):
        type = str(input("Enter type of Account(Savings/Recurring): "))
        branch = int(input("Enter Branch Pincode: "))
        amount = int(input("Enter initial Deposit: "))
        SCF.OpenAccount(mydb, cust_id, type, branch, amount)
    else:
        print("Invalid Customer ID!")
    
    EntryOptions()


def login():
    account_number = str(input("Enter Account Number: "))
    if SCF.CheckAccount(mydb, account_number) and SCF.CheckPassword(mydb, account_number):
        print("Account Found!")
        BankBasedOptions(account_number)
    elif not SCF.CheckAccount(mydb, account_number):
        print("Invalid Account Number!")
        EntryOptions()
    else:
        print("Invalid Password!")
        EntryOptions()



def BankBasedOptions(acc_no:int):
    while True:
        print("Select an option from below")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Show Details")
        print("4. Show Statements")
        print("5. Send Money")
        print("6. Exit")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            amount = int(input("Enter amount to be deposited: "))
            SCF.Transaction(mydb, acc_no, amount)

        elif choice == 2:
            amount = int(input("Enter amount to be withdrawn: "))
            SCF.Transaction(mydb, acc_no, -amount)

        elif choice == 3:
            # SCF.PrintTable(mydb, "Account", acc_no)
            # arr = SCF.PrintTable(mydb, "Account", acc_no)
            # for ele in arr[0]:
            #     print(ele)
            SCF.PrintDetails(mydb, acc_no)
            print()

        elif choice == 4:
            SCF.ShowStatements(mydb, acc_no)

        elif choice == 5:
            payee = int(input("Enter Payee Account Number: "))
            amount = int(input("Enter Amount to be Transferred: "))
            SCF.SendMoney(mydb, acc_no, payee, amount)

        elif choice == 6:
            print("\n\n")
            EntryOptions()



def EntryOptions():
    print(f"\n********** Welcome **********")
    choice = int(input("If you have an account, enter \"1\"\n"
                        "If you want to open an account, enter \"2\"\n"
                        "To exit the Bank, enter \"0\"\n"
                        "Enter your choice: "))

    if choice==1:
        login()
    elif choice==2:
        option = int(input("Are you an existing Customer?(1/0): "))
        if option==1:
            cust_id = int(input("Enter Customer ID: "))

            if SCF.CheckCustomer(mydb, cust_id):
                CreateAccount()
            else:
                print("\nCustomer ID Invalid!\n")
                EntryOptions()
        
        else:
            option = int(input("Do you want to become a Customer?(1/0): "))
            if option==1:
                name = str(input("Enter Full Name: "))
                DOB = str(input("Enter Date of Birth (DD-MM-YYYY): "))
                SCF.AddCustomer(mydb, name, DOB)
                
            EntryOptions()
        
    elif choice==0:
        exit()
    else:
        exit()

passwd = getpass("Enter Password to connect to database: ")

mydb = SCF.connect_server("localhost", "Shambhu Kaka", passwd)
EntryOptions()