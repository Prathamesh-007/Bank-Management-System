from fileinput import close
import os
from pathlib import Path
from queue import Full
import sys

path = str(os.getcwd())
path+="\Python-Bank-Project\Accounts"
print(path)


def FullPath(file_name:str)->str:
    # path = "C:/Users/Hp/Desktop/PYTHON/Trial folder/"
    file_name+=".txt"
    complete = os.path.join(path,file_name)
    return complete

abc = FullPath("LastAccNumber.txt")
print(abc)


def FileCheck(file_name:str) ->bool:
    """
    Function to check if a file exists in a predefined path

    Args:
        file_name (str): Name of the file whose existence is to be checked in pre-defined path

    Returns:
        bool: Returns 1 if file exists, else returns 0 if file doesn't exist
    """
    
    # path = "C:/Users/Hp/Desktop/PYTHON/Trial folder/"
    file_name+=".txt"
    complete = os.path.join(path,file_name)
    print(complete)
    if os.path.isfile(complete):
        return 1
    else:
        return 0

print()
print(FileCheck(abc))
    
def ReadFromFile(file_name:str):
    """

    Args:
        file_name (str): Name of the file which has the info of client

    Returns:
        name (str): Name of client according to the file
        acc_no (str): Account Number of client according to the file
        balance (int): Balance of the account according to the file
        transactions (list): Transactions of the client according to the file
    """
    
    
    # path = "C:/Users/Hp/Desktop/PYTHON/Trial folder/"
    file_name+=".txt"
    complete = os.path.join(path,file_name)

    count = int(0)
    transactions = []
    name = str()
    acc_no = int()
    balance = int()

    with open(complete) as file:
        count = int(0)
        data = file.readlines()
        for line in data:
            if count==0:
                name = str(line).rstrip("\n")
            elif count==1:
                acc_no = str(line).rstrip("\n")
            elif count==2:
                balance = int(line)
            else:
                transaction = str(line).rstrip("\n")
                transactions.append(transaction)

            count+=1
    # sys.stdin = open(complete,"r")
    # name = str(input())
    # acc_no = str(input())
    # balance = int(input())
    # while True:
    #     try:
    #         transaction = str(input())
    #         transactions.append(transaction)
    #     except EOFError:
    #         break
    
    return(name,acc_no, balance, transactions)



def WriteToFile(file_name:str, name:str, acc_no:str, balance:int, transaction_list:list)->None:
    complete = FullPath(file_name)
    balance = str(balance)
    with open(complete,"w") as file:
        file.write(name)
        file.write("\n")
        file.write(acc_no)
        file.write("\n")
        file.write(balance)
        file.write("\n")
        for transaction in transaction_list:
            file.write(transaction)
            file.write("\n")



def CreateNewFile(name:str, acc_no:str, balance:str, transaction_list:list)->None:
    complete = FullPath(acc_no)
    balance = str(balance)
    with open(complete,"w") as file:
        file.write(name)
        file.write("\n")
        file.write(acc_no)
        file.write("\n")
        file.write(balance)
        file.write("\n")
        for transaction in transaction_list:
            file.write(transaction)
            file.write("\n")
    
    return None
    
    

####### Trial Run for Checking and Debug Purposes #######
# f = str(input("Enter file name: "))
# if FileCheck(f):
#     print("Yes")
# else:
#     print("No")

