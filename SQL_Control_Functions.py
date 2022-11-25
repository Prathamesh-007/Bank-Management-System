# from ast import Interactive
import datetime
# from sqlite3 import connect
# from mysql import connector as mycon
import mysql.connector as mycon
from mysql.connector import Error
from getpass import getpass
from hashlib import sha1


def PasswordCreate()->str:
    """Function to Create a Password for an Account

    Returns:
        str: Returns the newly created password
    """
    flag = bool()
    while True:
        password = str(getpass("Enter a Password: "))
        confirm = str(getpass("Enter again to confirm: "))
        if confirm == password:
            flag = True

        if flag == True:
            return password
        else:
            print("Password not same!")


def CheckPassword(connection:mycon.connection.MySQLConnection ,acc_no:str)->bool:
    """Function to Check if the Entered Password is Correct

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        acc_no (str): Account Number whose Password is to be Checked

    Returns:
        bool: Returns True if Enter Password is Correct, else False
    """
    entered_pwd = str(getpass("Enter password: "))
    command = str(f"select *from Account where acc_no = {acc_no}")
    cursor = connection.cursor()
    cursor.execute(command)
    arr = cursor.fetchall()
    actual_pwd = arr[0][5]
    if sha1(entered_pwd.encode()).hexdigest() == actual_pwd:
        return True
    else:
        return False



def connect_server(host_name:str, user_name:str, password:str)->mycon.connection.MySQLConnection:
    """Function to connect with a MySQL Database

    Args:
        host_name (str): Name of the host of database
        user_name (str): name of the user of database
        password (str): password of the database
        dbname (str): Name of the database(tables)

    Returns:
        mycon.connection.MySQLConnection: MySQL connection object
    """
    connection = None
    try:
        connection = mycon.connect(host = host_name,
        user = user_name,
        passwd = password, 
        database = "Bank")
        print("Successfully Connected to Database!")

    except Error as err:
        print(f"Error: '{err}'")

    return connection



def Command_Execute(connection:mycon.connection.MySQLConnection, command:str)->None:
    """Function to execute the SQL command passed to it

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        command (str): Command to be executed
    """
    cursor = connection.cursor()

    try:
        cursor.execute(command)
        connection.commit()
        print("Query Executed Successfully!")
    except Error as err:
        print(f"Error: '{err}'")




def AddCustomer(connection:mycon.connection.MySQLConnection, name:str, DOB:str)->None:
    """Function to add a New Customer to Database

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        name (str): Name of the Customer to be added
        DOB (str): Date of Birth of the Customer
    """
    command = str("insert into Customer(name, DOB) values('" + name + "',' " + DOB + "')")
    # print(command)
    Command_Execute(connection, command)
    command = str("select *from Customer order by cust_id DESC limit 1;")
    cursor = connection.cursor()
    cursor.execute(command)
    arr = cursor.fetchall()
    print(f"Your Customer ID is: {arr[0][0]}")
    return arr[0][0]


def AlterBranch(connection:mycon.connection.MySQLConnection, branch:int, inc_dec:int)->None:
    """Function to Increment the Count of Accounts in a Branch

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        branch (int): Branch in which an Account has been Opened or Closed
        inc_dec (int): If Account Opened then =+1, Else =-1
    """

    command = str(f"update Branch set total_accounts = total_accounts + ({inc_dec}) where branch_id = {str(branch)}")
    print(command)
    Command_Execute(connection, command)


def OpenAccount(
    connection:mycon.connection.MySQLConnection,
    cust_id:int,
    type:str, branch:int, init:int, password:str = "")->None:
    """Function to Open a New Account

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        cust_id (int): Unique Cutomer ID given to each Customer
        type (str): Type of Account (e.g. Savings, Recurring)
        branch (int): Branch in which the Account is opened
        init (int): Initial Deposit in the Account
    """
    
    if password=="":
        password = PasswordCreate()

    command = "insert into Account(cust_id, type, branch_id, balance, password) values('"+ str(cust_id) + "', '" + type + "', '" + str(branch) + "', '" + str(init) + "', '" + sha1(password.encode()).hexdigest() + "');"
    print(command)
    Command_Execute(connection, command)
    AlterBranch(connection, branch, +1)
    command = str("select *from Account order by acc_no DESC limit 1;")
    cursor = connection.cursor()
    cursor.execute(command)
    arr = cursor.fetchall()
    print(f"Your Customer ID is: {arr[0][0]}")
    return arr[0][0]


def CheckCustomer(connection:mycon.connection.MySQLConnection, cust_id:int)->bool:
    command = str(f"select exists(select *from Customer where cust_id = {cust_id});")
    cursor = connection.cursor()
    cursor.execute(command)
    myresult = cursor.fetchall()
    return bool(myresult[0][0])



def DeleteEntry(connection:mycon.connection.MySQLConnection, acc_no:int)->None:
    """Function to Delete an Account

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        acc_no (int): Number of the Account which is to be deleted
    """
    cursor = connection.cursor()
    command = str(f"Select branch_id from Account where acc_no = {acc_no}")
    cursor.execute(command)
    branch = cursor.fetchall()
    if CheckPassword(connection, acc_no):
        command = str(f"delete from Account where id = {acc_no};")  
        Command_Execute(connection, command)
        AlterBranch(connection, branch, -1)
    else:
        print("Invalid password!")
        return



def PrintTable(connection:mycon.connection.MySQLConnection, table:str, acc_no:int)->list:
    """Function to print table

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        table (str): Name of the table to be displayed

    Returns:
        list: Returns List of the elements
    """
    cursor = connection.cursor()
    cursor.execute(f"select *from {table} where acc_no = {acc_no}")
    myresult = cursor.fetchall()
    # for row in myresult:
    #     print(row)
    #     break
    # print(myresult)
    return myresult


def CheckAccount(connection:mycon.connection.MySQLConnection, acc_no:int)->bool:
    """Function to Check if an Account is Present in Accounts Table

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        acc_no (int): Account Number whose presence is to be checked

    Returns:
        bool: Returns 1 if Account is Present, Else 0
    """
    command = str(f"select exists(select *from Account where acc_no = {acc_no});")
    cursor = connection.cursor()
    cursor.execute(command)
    myresult = cursor.fetchall()
    return(bool(myresult[0][0]))



def Statement(connection:mycon.connection.MySQLConnection, acc_no:int, amount:int):
    now = datetime.datetime.now()
    command = str(f"insert into Statements values({acc_no}, '{now.day}-{now.month}-{now.year}', '{now.hour}:{now.minute}:{now.second}', '{str(amount)}')")
    print(command)
    Command_Execute(connection, command)


def CheckBalance(connection:mycon.connection.MySQLConnection, acc_no:int, amount:int)->bool:
    command = str(f"select *from Account where acc_no = {acc_no};")
    cursor = connection.cursor()
    try:
        cursor.execute(command)
        arr = cursor.fetchall()
        balance = arr[0][4]
        if balance>=(-1*amount):
            return 1
        return 0
    except Error as err:
        print(f"Error: {err}")


def Transaction(connection:mycon.connection.MySQLConnection, acc_no:int, amount:int)->None:
    if CheckAccount(connection, acc_no):
        command = str("Update Account set balance = balance + (" + str(amount) + ") where acc_no = " + str(acc_no) )
        print(command)
        if CheckBalance(connection, acc_no, amount):
            print("Sufficient Amount")
        else:
            print("Insufficient Balance")
            return False
        Command_Execute(connection, command)
        # now = datetime.datetime.now()
        # command = str(f"insert into Statements values({acc_no}, '{now.day}-{now.month}-{now.year}', '{now.hour}:{now.minute}:{now.second}', '{str(amount)}')")
        # print(command)
        # Command_Execute(connection, command)
        Statement(connection, acc_no, amount)
        return True
    else:
        print(f"No Account {acc_no} present")
        return False


def SendMoney(connection:mycon.connection.MySQLConnection, payer:int, payee:int, amount:int):
    if CheckAccount(connection, payer) and CheckAccount(connection, payee):
        if CheckPassword(connection, payer):
            if(Transaction(connection, payer, (-1*amount))):
                Transaction(connection, payee, amount)
        else:
            print("Wrong password!")
            return
    else:
        print(f"Payer/Payee account number Invalid!")



def PrintDetails(connection:mycon.connection.MySQLConnection, acc_no:int):
    cursor = connection.cursor()
    cursor.execute(f"select *from Account where acc_no = {acc_no}")
    arr = cursor.fetchall()
    type = str(arr[0][1])
    cust_id = int(arr[0][2])
    branch_id = int(arr[0][3])
    balance = int(arr[0][4])
    result = [type, cust_id, branch_id, balance]
    
    cursor.execute(f"select *from Customer where cust_id = {cust_id}")
    arr = cursor.fetchall()
    name = str(arr[0][1])
    result.append(name)

    print(f"Name: {name}")
    print(f"Customer ID: {cust_id}")
    print(f"Account Number: {acc_no}")
    print(f"Balance: {balance}")
    print(f"Branch ID: {branch_id}")
    print()
    return result
    

def ShowStatements(connection:mycon.connection.MySQLConnection, acc_no:int):
    cursor = connection.cursor()
    cursor.execute(f"select *from Statements where acc_no = {acc_no}")
    arr = cursor.fetchall()
    print("Acc_no |   date   |    time    | amount")
    for i in arr:
        print(i)
    
    return arr



#
#
#
#
#
#
def CheckPassword2(connection:mycon.connection.MySQLConnection ,acc_no:str, entered_pwd:str)->bool:
    """Function to Check if the Entered Password is Correct

    Args:
        connection (mycon.connection.MySQLConnection): Connection made with the SQL database
        acc_no (str): Account Number whose Password is to be Checked

    Returns:
        bool: Returns True if Enter Password is Correct, else False
    """
    # entered_pwd = str(getpass("Enter password: "))
    command = str(f"select *from Account where acc_no = {acc_no}")
    cursor = connection.cursor()
    cursor.execute(command)
    arr = cursor.fetchall()
    actual_pwd = arr[0][5]
    if sha1(entered_pwd.encode()).hexdigest() == actual_pwd:
        return True
    else:
        return False


def SendMoney2(connection:mycon.connection.MySQLConnection, payer:int, payee:int, amount:int, password:str):
    if CheckAccount(connection, payee):
        if CheckPassword2(connection, payer, password):
            if(Transaction(connection, payer, (-1*amount))):
                Transaction(connection, payee, amount)
                return "All Correct"
            else:
                return "Insufficient Amount"
        else:
            print("Wrong password!")
            return "Wrong Password"   
    else:
        print(f"Payee account number Invalid!")
        return "Invalid Payee"