import SQL_Control_Functions as SCF
from getpass import getpass
from hashlib import sha1

mydb = SCF.connect_server("localhost", "root", "shree_123")

# SCF.AddCustomer(mydb, "Sachhidanand Shrikrishna Sahasrabuddhe", "17-04-1964")

# SCF.OpenAccount(mydb, 101, "Savings", 411038, 15000)

# password = SCF.PasswordCreate()

# password = getpass("Enter password: ")
# print(password)

# arr = SCF.PrintTable(mydb, "Account")

# print(arr)

# branch = arr[0][3]

# SCF.AlterBranch(mydb, branch)


# password = str(input("Enter Password: "))

# if arr[0][5] == sha1(password.encode()).hexdigest():
#     amount = int(input("Enter amount to be withdrawn: "))
#     SCF.Transaction(mydb, 1, amount)

# print(SCF.CheckPassword(mydb, 1))

# print(sha1("Abcd".encode()).hexdigest())

# SCF.SendMoney(mydb, 1000, 1010, 1500)
SCF.PrintTable(mydb, "Statements")

# SCF.Transaction(mydb, 1010, -500)
# arr = SCF.CheckAccount(mydb, 1010)
# print(arr)